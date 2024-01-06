import subprocess
import time
from datetime import datetime
import os

import pathlib 
from decouple import Config, RepositoryEnv
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def run_ps_cmd(cmd: list[str], log: bool=True):
    all_outputs = []
    try:
        full_cmd = ['powershell', '-Command'] + cmd
        full_cmd_str = " ".join(cmd)
        if log: print(f"Running command: {full_cmd_str}\n")
        result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        combined_output = result.stdout + result.stderr
        output = combined_output.strip()
        if log: print(f"Output: {output}\n")
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to run PowerShell command. Exit Code {e.returncode}\n")
        raise 

def auth(email: str):
    output = run_ps_cmd(['gcloud', 'auth', 'list', '--format=json'], log=False)
    output_json = json.loads(output.replace("\n", ""))
    for account in output_json:
        if account["account"] == email:
            if account["status"] == "ACTIVE":
                print("Authenticated as "+email)
                return
            else:
                run_ps_cmd(['gcloud', 'auth', 'login', email], log=False)
                print("Authenticated as "+email)
                return
    run_ps_cmd(['gcloud', 'auth', 'login'])

def link_billing_account(proj_id):
    # Get billing accounts lists
    output = run_ps_cmd(['gcloud', 'alpha', 'billing', 'accounts', 'list', '--format=json'], log=False)
    output_json = json.loads(output.replace("\n", ""))
    bill_acc_id = output_json[0]["name"].split("/")[-1]
    # Link billing account to project
    run_ps_cmd(['gcloud', 'alpha', 'billing', 'projects', 'link', f'{proj_id}', f'--billing-account={bill_acc_id}'])

def init(email: str=None, proj_name: str="wweb-scrapingg", base_path: str=None):

    if email == None:        
        # get variable from .env file in the project's root directory
        BASE_DIR = pathlib.Path(__file__).parent
        ENV_PATH = BASE_DIR / '.env'
        env_config = Config(RepositoryEnv(ENV_PATH))
        email = env_config.get('email')

    if base_path == None:        
        base_path = os.path.join(os.getcwd(), "sa_key")
        if not os.path.exists(base_path):
            os.makedirs(base_path)
    
    auth(email)
    
    # Create project
    time_iso_now = datetime.utcnow().isoformat() # current ISO time
    time_iso_now = time_iso_now.replace(".", "").replace("T", "").replace(":", "").replace("-", "") # remove special characters from ISO time
    proj_id = f"{proj_name}-{time_iso_now}"[:30] # project id
    run_ps_cmd(['gcloud', 'projects', 'create', proj_id, f"--name={proj_name}"])
    
    # Link billing account
    try:
        link_billing_account(proj_id)
    except:
        print("Could not link billing account to project. Please do it manually.")
    
    # Enable services API
    services = ['serviceusage', 'cloudresourcemanager', 'iam', 'compute']
    for service in services:
        run_ps_cmd(['gcloud', 'services', 'enable', f'{service}.googleapis.com', f'--project={proj_id}'])
    
    # Create service account, grant owner role and create credentials file
    key_path = os.path.join(base_path, "credentials.json") # path to save the credentials file
    sa_email = f'{proj_name}@{proj_id}.iam.gserviceaccount.com'
    run_ps_cmd(['gcloud', 'iam', 'service-accounts', 'create', proj_name, f"--project={proj_id}"])
    run_ps_cmd(['gcloud', 'projects', 'add-iam-policy-binding', proj_id, f'--member=serviceAccount:{sa_email}', '--role=roles/owner'])
    run_ps_cmd(['gcloud', 'iam', 'service-accounts', 'keys', 'create', f'"{key_path}"', f'--iam-account={sa_email}', f"--project={proj_id}"])
    
    
if __name__ == "__main__":
    init()