from flask import Flask
from app.extensions import db
from app.models.Run import Run
from app.models.Post import Post
from utils.time import get_time


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:alex@localhost/job"
db.init_app(app)

with app.app_context():
    # row = Run.query.filter_by(id=1).first()
    db.create_all()
    row = Run(slave="slave", project_token="project_token", run_token="run_token", status="status", md5sum="md5sum", start_url="start_url", start_value={}, updated=get_time())
    db.session.add(row)
    db.session.commit()
