from flask import current_app as c_app
from sqlalchemy import select

from ..models import Post


def remove_existing_posts(data: dict) -> None:
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        for i in range(len(data["job_post"])):
            
            post_exists = db.session.query(select(1).filter(
                Post.description == data["job_post"][i][Post.description.key]
            ).exists()).scalar()
            
            if post_exists:
                del data["job_post"][i]