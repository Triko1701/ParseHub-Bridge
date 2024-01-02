import json

from app.task import app_celery
from app.services.db import insert_data, update_run
from app.services.parsehub import get_run_data
from app.task.waiting_run_triggering import trigger_a_waiting_run


@app_celery.task
def process_webhook(request):
    # with app.app_context():
    options_json_string = request.form.get('options_json')
    run_token = request.form.get('run_token')
    status = request.form.get('status')
    data_ready = request.form.get('data_ready')
    md5sum = request.form.get('md5sum')
    new_run = request.form.get('new_run')
    
    if status == 'error': # ERROR
        if new_run:
            new_run_dict = json.loads(new_run)
            new_run_token = new_run_dict.get("run_token") # new_run_token
            if new_run_token: # update the run_token, update the status to waiting
                update_run({"run_token": run_token}, {"run_token": new_run_token, "status": "waiting", "md5sum": md5sum})
            else:
                update_run({"run_token": run_token}, {"run_token": "new_run_error", "status": "new_run_error", "md5sum": md5sum})
        else: # update the status to unknown error
            update_run({"run_token": run_token}, {"status": "unknown_error", "md5sum": md5sum})
            
    elif status == 'complete': # COMPLETE
        data = get_run_data(run_token=run_token) # Get data
        insert_data(data) # Insert data to DB
        update_run({"run_token": run_token}, {"status": "complete", "md5sum": md5sum}) # Update the status to complete
        trigger_a_waiting_run() # Trigger a waiting run if exist

    else: # OTHER
        update_run({"run_token": run_token}, {"status": status, "md5sum": md5sum}) # update status