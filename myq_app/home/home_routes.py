from flask import Blueprint, render_template, url_for, redirect
from flask import current_app as app
from .models import Queue, db
from .forms import QueueForm, FindQueueForm, EnterQueueForm

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=['POST', 'GET'])
def index():
    cForm = QueueForm()
    fForm = FindQueueForm()
    eForm = EnterQueueForm()

    if cForm.validate_on_submit():
        new_name = cForm.name.data
        new_passkey = cForm.passkey.data
        new_max_quantity = cForm.max_quantity.data
        new_queue = Queue(queue_name=new_name, passkey=new_passkey, max_quantity=new_max_quantity)

        try:
            db.session.add(new_queue)
            db.session.commit()
            return redirect(url_for('home_bp.index'))
        except:
            return 'There was an issue adding a queue'

    if fForm.validate_on_submit():
        find_name = fForm.name.data
        find_passkey = fForm.passkey.data
        toFind = Queue.query.filter(Queue.queue_name == find_name).first()
        if(toFind is not None):
            if(toFind.passkey == find_passkey):
                return redirect(url_for('queue_bp.queue_admin', queue_id=toFind.id))
    
    if eForm.validate_on_submit():
        enter_name = eForm.name.data
        toEnter = Queue.query.filter(Queue.queue_name == enter_name).first()
        if(toEnter is not None):
            return redirect(url_for('queue_bp.queue', queue_id=toEnter.id))

    cForm.name.data = ""
    cForm.passkey.data = ""
    cForm.max_quantity.data = ""
    fForm.name.data = ""
    fForm.passkey.data = ""
    eForm.name.data = ""
    return render_template('index.html', cForm=cForm, fForm=fForm, eForm=eForm)

