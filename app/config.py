from utils.metadata import get_custom_metadata
from utils.gce import get_db_ip


db_ip = get_db_ip()
db_user, db_password, db_name = get_custom_metadata(
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB"
    )

class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_ip}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    