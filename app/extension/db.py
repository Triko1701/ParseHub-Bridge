from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def db_init_app(app: Flask) -> SQLAlchemy:
    db = SQLAlchemy()
    db.init_app(app)
    app.extensions["sqlalchemy"] = db
    return db
    