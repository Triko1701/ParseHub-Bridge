from flask import current_app as c_app
from celery import shared_task

from utils import get_dict_field

from ..services import insert_data, update_run, get_run_data, trigger_waiting_runs, remove_existing_posts
from ..models import RunStatus, Run


@shared_task.task
def process_webhook(status: str, run_token: str, md5sum: str, new_run, created_at: str):
    
    new_run_token = get_dict_field(new_run, Run.run_token.key)
    new_status = get_dict_field(new_run, Run.status.key)
    
    if status == RunStatus.ERROR:
        if new_run: # new_run
            if new_run_token:
                update_run(run_token, new_status, md5sum, new_run_token)
            else:
                update_run(run_token, RunStatus.NEW_RUN_TOKEN_MISSED, md5sum)

        else: # unknown error
            update_run(run_token, status, md5sum)
            
    elif status == RunStatus.COMPLETE:
        data = get_run_data(run_token=run_token)
        remove_existing_posts(data)
        insert_data(data)
        update_run(run_token, status, md5sum)
        trigger_waiting_runs()

    else: # OTHER STATUS
        if new_run:
            if new_run_token:
                update_run(run_token, new_status, md5sum, new_run_token)
            else:
                update_run(run_token, RunStatus.NEW_RUN_TOKEN_MISSED, md5sum)
        else:
            update_run(run_token, status, md5sum)
        
    
    return {
        "status": status,
        "run_token": run_token,
        "md5sum": md5sum,
        "new_run": new_run,
        "created_at": created_at
    }