from utils.metadata_extraction import get_custom_metadata
from utils.gce import get_db_ip


try:
    db_user, db_password, db_name = get_custom_metadata(
                                                           "POSTGRES_USER",
                                                           "POSTGRES_PASSWORD",
                                                           "POSTGRES_DB",
                                                           )
    db_ip = get_db_ip()
except:
    db_ip = "localhost"
    user = "postgres"
    passwd = "alex"
    db_name = "job"

class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_ip}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    