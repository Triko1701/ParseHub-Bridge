from flask import current_app as c_app

from ...models import Run

                
def update_run(run_token: str, status: str, md5sum: str, new_run_token: str=None) -> None:
    update_dict = {
        Run.status.key: status,
        Run.md5sum.key: md5sum,
    }
    if new_run_token:
        update_dict[Run.run_token.key] = new_run_token
        
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        db.session.query(Run).filter(Run.run_token == run_token).update(update_dict)
