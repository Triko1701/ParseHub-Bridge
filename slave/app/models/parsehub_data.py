from sqlalchemy import JSON
from sqlalchemy import DateTime

from app import db, Base


class Run(Base):
    __tablename__ = 'run'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slave = db.Column(db.String(100))
    project_token = db.Column(db.String(100))
    run_token = db.Column(db.String(100))
    status = db.Column(db.String(50), default="waiting")
    md5sum = db.Column(db.TEXT)
    start_url = db.Column(db.Text)
    start_value = db.Column(db.JSON)
    insert_time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Run token {self.run_token}>"


class Post(Base):
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
    employer_questions = db.Column(db.Text[])
    insert_time = db.Column(db.DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Job post url {self.job_url}>"
    
    
# class Job(Base):
#     __tablename__ = 'job_listings'

#     job_url = db.Column(db.String(255))

#     title = db.Column(db.String(255))
#     advertiser = db.Column(db.String(255))
#     location = db.Column(db.String(255))
#     category = db.Column(db.String(255))
#     job_type = db.Column(db.String(255))
#     salary = db.Column(db.String(255))
#     time_posted = db.Column(db.String(255))

#     description = db.Column(db.Text)
#     employer_questions = db.Column(db.Text)

#     title_words = db.Column(db.ARRAY(db.Text))
#     description_words = db.Column(db.ARRAY(db.Text))
#     employer_questions_words = db.Column(db.ARRAY(db.Text))
