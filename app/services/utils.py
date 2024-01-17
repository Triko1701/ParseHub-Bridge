from flask import current_app as c_app

from ..models import Post


def remove_existing_posts(data: dict) -> None:
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        for i in range(len(data["job_post"])):
            post_existing = db.session.query(Post).filter(
                Post.description == data["job_post"][i][Post.description.key]
            ).exists()
            if bool(post_existing):
                del data["job_post"][i]