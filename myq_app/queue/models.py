from myq_app import db
from datetime import datetime

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    queue_number = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    queue_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Member %r>' % self.id