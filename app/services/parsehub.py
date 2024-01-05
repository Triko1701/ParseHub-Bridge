import requests

from ...utils.vm_metadata_extraction import get_vm_meta
from ..models.Run import Run
from ..extensions import db

def trigger_run(api_key, project_token, start_url, start_template=None, start_value_override=None):
    url = f"https://www.parsehub.com/api/v2/projects/{project_token}/run" # url
    # parameters
    params = {
        "api_key": api_key,
        "start_url": start_url,
        "start_value_override": start_value_override,
        "send_email": "1"
    }
    
    try:
        response = requests.post(url, data=params) # response
        if response.ok:
            return response.json()
        print(f"Error: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None


def get_run_data(api_key, run_token, data_format='json'):
    url = f'https://www.parsehub.com/api/v2/runs/{run_token}/data' # url
    params = {"api_key": api_key, "format": data_format} # params
    
    try:
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()
        print(f"Error: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return None


def trigger_waiting_runs(n: int=1):
    # Get necessary parameters
    VM_name, api_key, project_token = get_vm_meta(VM_name, api_key, project_token)
    
    # Get waiting runs
    runs_to_be_triggered = Run.query.filter_by(slave=VM_name, status='waiting').all()
    
    # Trigger the run(s)
    n = min(n, len(runs_to_be_triggered))
    for i in range(n):
        run = runs_to_be_triggered[i]
        try:
            trigger_run(api_key, project_token, run.start_url)
            run.status = 'queued'
            print(f"Triggered the run {run.id}")
        except:
            print(f"Failed to trigger the run {run.id}")
            run.status = 'trigger_error'
    db.session.commit()