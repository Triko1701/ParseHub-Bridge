from itertools import islice

from flask import current_app as c_app

from ...models import Post


def insert_data(data: dict, batch_size: int=50) -> None:
    def post_generator():
        for post in data["job_post"]:
            post[Post.employer_questions.key] = post[Post.employer_questions.key].split("||")
            yield post

    generator = post_generator()
    db = c_app.extensions["sqlalchemy"]
    while True:
        batch = list(islice(generator, batch_size))
        
        if not batch:
            break
        
        with db.session.begin():
            db.session.bulk_insert_mappings(Post, batch)

