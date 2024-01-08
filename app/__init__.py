from flask import Flask


def create_app():
    app = Flask(__name__)
    
    from .config.config import Config
    app.config.from_object(Config)
    
    from .routes.webhook import webhook_blueprint
    app.register_blueprint(webhook_blueprint)
    
    from .extensions import db
    db.init_app(app)
    
    return app
