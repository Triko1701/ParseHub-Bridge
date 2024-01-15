from flask import Flask
from logging.handlers import RotatingFileHandler
from utils import create_file


def create_app() -> Flask:
    # Set logging config
    from .config import Config
    create_file(Config.LOG_FILE_PATH)
    file_handler = RotatingFileHandler(Config.LOG_FILE_PATH)

    app = Flask(__name__)
    app.logger.addHandler(file_handler)
    app.config.from_object(Config)
    
    from .extension import celery_init_app, db_init_app
    db_init_app(app)
    celery_init_app(app)
    
    from .routes import webhook_blueprint
    app.register_blueprint(webhook_blueprint)
    
    return app
