from myq_app import db
from datetime import datetime

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_name = db.Column(db.String(100), nullable=False)
    passkey = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, default=0)
    max_quantity = db.Column(db.Integer, nullable=False)
    lastNo_added = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="Open")
    image_link = db.Column(db.String(500), nullable=True, default="None")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Queue %r>' % self.id