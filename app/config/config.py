from utils.vm_metadata_extraction import get_vm_metadata_field
import json

# db_info = json.loads(get_vm_metadata_field("db_info"))
db_info = {
    'ip': 'localhost',
    'user': 'postgres',
    'password': 'alex',
    'name': 'job'
}
db_ip = db_info.get('ip')
db_user = db_info.get('user')
db_password = db_info.get('password')
db_name = db_info.get('name')

class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_ip}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    