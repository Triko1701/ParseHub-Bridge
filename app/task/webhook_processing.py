import json

from . import app_celery
from ..services.db import insert_data, update_run
from ..services.parsehub import get_run_data, trigger_waiting_runs


@app_celery.task
def process_webhook(form_data):
    
    status = form_data.get('status')
    run_token = form_data.get('run_token')
    md5sum = form_data.get('md5sum')
    new_run = form_data.get('new_run')
    
    if status == 'error': # ERROR
        
        if new_run: # new_run
            new_run_dict = json.loads(new_run)
            new_run_token = new_run_dict.get("run_token")
            
            # update the run_token and status
            if new_run_token:
                status = "waiting"
            else:
                status = "new_run_token_not_found"
                new_run_token = run_token
            update_run({"run_token": run_token}, {"run_token": new_run_token, "status": status, "md5sum": md5sum})
        
        else: # unknown error
            update_run({"run_token": run_token}, {"status": "unknown_error", "md5sum": md5sum})
            
            
    elif status == 'complete': # COMPLETE
        data = get_run_data(run_token=run_token)
        insert_data(data)
        update_run({"run_token": run_token}, {"status": "complete", "md5sum": md5sum})
        trigger_waiting_runs()


    else: # OTHER STATUS
        update_run({"run_token": run_token}, {"status": status, "md5sum": md5sum}) # update status