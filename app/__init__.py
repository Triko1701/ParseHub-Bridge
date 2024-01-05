from flask import Flask

from .extensions import db
from .config.config import Config
from .routes.webhook import webhook_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(webhook_blueprint)
    app.config.from_object(Config)
    db.init_app(app)
    return app
    
    # Import models within the application context to avoid circular import
    # with app.app_context():
    #     from app.models.Run import Run
    #     from app.models.Post import Post
        
    #     db.create_all() 
            