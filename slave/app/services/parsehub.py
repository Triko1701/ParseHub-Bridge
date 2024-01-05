import requests


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
