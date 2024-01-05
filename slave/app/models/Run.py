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