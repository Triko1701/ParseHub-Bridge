import socket

from utils import get_user_metadata, get_vm_ext_ip

from ..models import Meta


MASTER_IP = get_vm_ext_ip("master")
USER = get_user_metadata(Meta.USER.value)
POSTGRES_PASSWORD = get_user_metadata(Meta.REDIS_PASSWORD.value)
PROJECT = get_user_metadata(Meta.PROJECT.value)
REDIS_PASSWORD = get_user_metadata(Meta.REDIS_PASSWORD.value)

class Config():
    # DEBUG = True
    # TESTING = True

    # Slave name, logging, default timezone
    SLAVE_NAME = socket.gethostname()
    LOG_FILE_PATH = "var/log/Parsehub/flask.log"
    DEFAULT_TIMEZONE = "Australia/Sydney"
    
    # Parsehub
    API_KEY = get_user_metadata(Meta.API_KEY.value)
    PROJ_TOKEN = get_user_metadata(Meta.PROJ_TOKEN.value)
    
    # Postgresl
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{POSTGRES_PASSWORD}@{MASTER_IP}/{PROJECT}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery
    CELERY = dict(
        broker_url = f"redis://:{REDIS_PASSWORD}@{MASTER_IP}/0",
        result_backend = "db+" + SQLALCHEMY_DATABASE_URI
    )