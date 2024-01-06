from flask import Flask
from app.extensions import db
from app.models.Run import Run


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:alex@localhost/job"
db.init_app(app)

with app.app_context():
    row = Run.query.filter_by(id=1).first()

print(type(row))
print(row)
print(row.result)
