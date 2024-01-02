from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()
Base = db.Model


from app.config.config import Config
from app.routes.webhook import webhook_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(webhook_blueprint)
    
    app.config.from_object(Config)

    db.init_app(app)
    
    # Import models within the application context to avoid circular import
    with app.app_context():
        from app.models.Run import Run
        from app.models.Post import Post
        
        db.create_all() 
            
    return app