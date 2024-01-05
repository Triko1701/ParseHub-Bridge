from sqlalchemy.dialects.postgresql import ARRAY

from ..extensions import db


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
    updated = db.Column(db.DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Job post url {self.job_url}>"