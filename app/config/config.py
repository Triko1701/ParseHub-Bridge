import socket

from ..utils import get_user_metadata, ComputeInstance
from ..models import Meta

master_instance = ComputeInstance("master")
MASTER_IP = master_instance.ext_ip
USER = get_user_metadata(Meta.USER.value)
POSTGRES_PASSWORD = get_user_metadata(Meta.POSTGRES_PASSWORD.value)
PROJECT = get_user_metadata(Meta.PROJECT.value)
REDIS_PASSWORD = get_user_metadata(Meta.REDIS_PASSWORD.value)

class MasterConfig(object):
    # DEBUG = True
    # TESTING = True    
    DEFAULT_TIMEZONE = "Australia/Sydney"
    LOG_FILE_PATH = f"var/log/{PROJECT}/flask.log"
    
    # Postgresl
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{POSTGRES_PASSWORD}@{MASTER_IP}/{PROJECT}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery
    CELERY = dict(
        broker_url = f"redis://:{REDIS_PASSWORD}@{MASTER_IP}/0",
        result_backend = "db+" + SQLALCHEMY_DATABASE_URI
    )    

class SlaveConfig(MasterConfig):
    @property
    def SLAVE_NAME():
        return socket.gethostname()
    
    @property
    def API_KEY():
        return get_user_metadata(Meta.API_KEY.value)
    
    @property
    def PROJ_TOKEN():
        return get_user_metadata(Meta.PROJ_TOKEN.value)
    

