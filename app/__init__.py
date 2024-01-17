from flask import Flask
from logging.handlers import RotatingFileHandler


def create_app(config_class=None, role: str="slave") -> Flask:
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    else:
        if role.lower()=="master":
            from .config import MasterConfig as Config
        elif role.lower()=="slave":
            from .config import SlaveConfig as Config
        from .utils import create_file
        create_file(Config.LOG_FILE_PATH)
        file_handler = RotatingFileHandler(Config.LOG_FILE_PATH)
        app.logger.addHandler(file_handler)
        app.config.from_object(Config)
    
    from .extension import celery_init_app, db_init_app
    db_init_app(app)
    celery_init_app(app)
    
    from .routes import webhook_blueprint, greeting_blueprint
    app.register_blueprint(webhook_blueprint)
    app.register_blueprint(greeting_blueprint)
    
    return app
