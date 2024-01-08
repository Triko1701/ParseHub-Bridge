from utils.vm_metadata_extraction import get_vm_metadata
import json

try:
    db_user, db_password, db_name, db_ip = get_vm_metadata("db_info")
except:
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
    