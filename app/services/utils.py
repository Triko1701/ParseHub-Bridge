from flask import current_app as c_app

from ..models import Post


def remove_existing_posts(data: dict) -> None:
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        for i in range(len(data["job_post"])):
            exists = db.session.query(Post).exists().filter(
                Post.description == data["job_post"][i][Post.description.key]
            )
            if exists:
                del data["job_post"][i]