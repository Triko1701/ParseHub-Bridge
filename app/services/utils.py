from flask import current_app as c_app
from sqlalchemy import select, and_

from ..models import Post


def remove_existing_posts(data: dict) -> None:
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        for i in range(len(data["job_post"])):
            
            post_exists = db.session.query(select(1).filter(
                and_(
                    Post.title == data["job_post"][i][Post.title.key],
                    Post.job_url == data["job_post"][i][Post.job_url.key],
                    Post.description == data["job_post"][i][Post.description.key]
                )
            ).exists()).scalar()
            
            if post_exists:
                del data["job_post"][i]