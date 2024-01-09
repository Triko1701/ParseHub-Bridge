from ..extensions import db


class Run(db.Model):
    __tablename__ = 'run'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slave = db.Column(db.String(100))
    run_token = db.Column(db.String(100))
    status = db.Column(db.String(50), default="waiting")
    md5sum = db.Column(db.TEXT)
    start_url = db.Column(db.Text)
    start_value = db.Column(db.JSON)
    updated = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Run ID {self.id}>"
    