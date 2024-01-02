from utils.vm_metadata_extraction import get_vm_meta_field
from app.models.Run import Run
from app.services.parsehub import trigger_run
from app import db


def trigger_a_waiting_run():
    # Get necessary parameters
    ext_ip, api_key, project_token = get_vm_meta_field(ext_ip, api_key, project_token)
    
    # Get a waiting run
    run_to_be_triggered = Run.query.filter_by(slave=ext_ip, status='waiting').first()
    
    # If no waiting run to be triggered
    if run_to_be_triggered:
        try:
            trigger_run(api_key, project_token, run_to_be_triggered.start_url)
            run_to_be_triggered.status = 'queued'
            db.session.commit()
            print(f"Triggered the run {run_to_be_triggered.id}")
        except:
            print(f"Failed to trigger the run {run_to_be_triggered.id}")
            run_to_be_triggered.status = 'trigger_error'
            db.session.commit()
    else:
        print("No waiting run to be triggered")
            
    