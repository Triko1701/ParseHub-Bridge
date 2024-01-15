from flask import current_app as c_app

from utils import get_current_time

from .run_status import RunStatus


current_time = lambda : get_current_time(c_app.config["DEFAULT_TIMEZONE"])
db = c_app.extensions["sqlalchemy"]

class Run(db.Model):
    __tablename__ = 'run'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slave = db.Column(db.String(100))
    run_token = db.Column(db.String(100))
    status = db.Column(db.String(50), default=RunStatus.WAITING)
    md5sum = db.Column(db.TEXT)
    start_url = db.Column(db.Text)
    start_value = db.Column(db.JSON, default={})
    updated_at = db.Column(db.DateTime(timezone=True), default=current_time, onupdate=current_time)

    def __repr__(self):
        return f"<Run ID {self.id}>"
    