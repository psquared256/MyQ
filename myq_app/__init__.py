from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    with app.app_context():
        
        from .home.models import Queue
        from .queue.models import Member
        db.create_all()

        from .home import home_routes
        from .queue import queue_routes

        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(queue_routes.queue_bp)

        
        
        return app