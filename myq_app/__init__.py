from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

def init_app():
    application = Flask(__name__, instance_relative_config=False)

    # Comment out ('config.Demo_Config') and comment in ('config.Config') to use the local database

    # application.config.from_object('config.Config')
    application.config.from_object('config.Demo_Config')
    
    db.init_app(application)

    with application.app_context():
        
        from .home.models import Queue
        from .queue.models import Member
        db.create_all()

        from .home import home_routes
        from .queue import queue_routes

        application.register_blueprint(home_routes.home_bp)
        application.register_blueprint(queue_routes.queue_bp)

        
        
        return application