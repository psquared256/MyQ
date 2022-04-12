from flask import Blueprint, redirect, url_for, render_template
from flask import current_app as app
from .models import Member, db
from myq_app.home.models import Queue
from .forms import MemberForm

queue_bp = Blueprint(
    'queue_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

#Admin functions

@queue_bp.route('/queue_admin/<int:queue_id>', methods=['POST', 'GET'])
def queue_admin(queue_id):
    to_show = Queue.query.get_or_404(queue_id)
    members = Member.query.order_by(Member.date_created).filter(Member.queue_id == queue_id).all()
    return render_template('queue_admin.html', queue=to_show, members=members)

@queue_bp.route('/queue_admin/<int:queue_id>/remove/<int:member_id>', methods=['POST', 'GET'])
def remove(queue_id, member_id):
    member_to_delete = Member.query.get_or_404(member_id)

    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        return redirect(url_for('queue_bp.queue_admin', queue_id=queue_id))
    except:
        return 'There was an error deleting the member'
    pass

@queue_bp.route('/queue_admin/<int:queue_id>/change_status', methods=['POST', 'GET'])
def change_status(queue_id):
    to_change = Queue.query.get_or_404(queue_id)
    if(to_change.status == "Open"):
        to_change.status = "Closed"
    else:
        to_change.status = "Open"

    try:
        db.session.commit()
        return redirect(url_for('queue_bp.queue_admin', queue_id=queue_id))
    except:
        return 'There was an problem changing queue status'

@queue_bp.route('/queue_admin/<int:queue_id>/delete', methods=['POST', 'GET'])
def delete(queue_id):
    to_delete = Queue.query.get_or_404(queue_id)
    try:
        clear_queue(queue_id=queue_id)
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for('home_bp.index'))
    except:
        return 'There was an error deleting your queue'

@queue_bp.route('/queue_admin/<int:queue_id>/clear', methods=['POST', 'GET'])
def clear(queue_id):
    Member.query.filter(Member.queue_id == queue_id).delete()
    try:
        clear_queue(queue_id=queue_id)
        return redirect(url_for('queue_bp.queue_admin', queue_id=queue_id))
    except:
        return 'There was an error deleting your queue'
    

def clear_queue(queue_id):
    members_to_delete = Member.query.filter(Member.queue_id == queue_id).all()

    for member in members_to_delete:
        db.session.delete(member)
    db.session.commit()

#Member functions

@queue_bp.route('/queue/<int:queue_id>', methods=['POST', 'GET'])
def queue(queue_id):
    aForm = MemberForm()
    toShow = Queue.query.get_or_404(queue_id)

    if aForm.validate_on_submit():
        find_name = aForm.name.data
        name_exists = Member.query.filter(Member.full_name == find_name, Member.queue_id == queue_id).first()
        
        if(name_exists is None):
            new_member_name = aForm.name.data
            new_member = Member(full_name=new_member_name, queue_id=queue_id)

            if(toShow.quantity < toShow.max_quantity and toShow.status == "Open"):
                if(toShow.lastNo_added == toShow.max_quantity):
                    new_member.queue_number = 1
                    toShow.lastNo_added = 1
                else:
                    new_member.queue_number = toShow.lastNo_added + 1
                    toShow.lastNo_added = toShow.lastNo_added + 1
                toShow.quantity = toShow.quantity + 1

                try:
                    db.session.add(new_member)
                    db.session.commit()
                    # return redirect(url_for('queue_bp.queue', queue_id=queue_id, number=new_member.queue_number))
                    return render_template('queue.html', queue=toShow, number=new_member.queue_number, form=aForm)

                except:
                    return 'There was an issue adding a member'
        else:
            # return redirect(url_for('queue_bp.queue', queue_id=queue_id, number=name_exists.queue_number))
            return render_template('queue.html', queue=toShow, number=name_exists.queue_number, form=aForm)

    
    return render_template('queue.html', queue=toShow, number=0, form=aForm)