from flask import current_app as c_app

from utils import get_dict_field

from ...models import Run, RunStatus, Meta
from .trigger_run import trigger_run


def trigger_waiting_runs(n: int=1) -> None:
    # Get necessary parameters
    api_key = c_app.config[Meta.API_KEY]
    project_token = c_app.config[Meta.PROJ_TOKEN]
    host_name = c_app.config["SLAVE_NAME"]
    
    # Get waiting runs
    waiting_runs = Run.query.filter_by(slave=host_name, status=RunStatus.WAITING.value).all()
    
    # Trigger the run(s)
    n = min(n, len(waiting_runs))
    count = 0
    index = 0
    db = c_app.extensions["sqlalchemy"]
    with db.session.begin():
        while (count < n) and (index < len(waiting_runs)):
            run = waiting_runs[index]
            index += 1

            try:
                r = trigger_run(api_key, project_token, run.start_url)
            except Exception as e:
                c_app.logger.error(f"Failed to trigger the run {run.id}, start_url {run.start_url} - {e}")
                run.status = RunStatus.TRIGGER_ERROR.value
                continue

            count += 1
            run_token = get_dict_field(r.json(), run.run_token.key)
            status = get_dict_field(r.json(), run.status.key)
            run.status = status if status else RunStatus.QUEUEDv
            run.run_token = run_token
