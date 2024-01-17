from sqlalchemy.dialects.postgresql import ARRAY
from flask import current_app as c_app

from ..utils import get_current_time
from ..extension import db


current_time = lambda : get_current_time(c_app.config["DEFAULT_TIMEZONE"])

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_url = db.Column(db.Text)
    title = db.Column(db.String(255))
    advertiser = db.Column(db.String(255))
    location = db.Column(db.String(255))
    category = db.Column(db.String(255))
    job_type = db.Column(db.String(255))
    salary = db.Column(db.String(255))
    time_posted = db.Column(db.String(255))
    description = db.Column(db.Text)
    employer_questions = db.Column(ARRAY(db.Text))
    updated_at = db.Column(db.DateTime(timezone=True), default=current_time, onupdate=current_time)
    
    def __repr__(self):
        return f"<Job post url {self.job_url}>"