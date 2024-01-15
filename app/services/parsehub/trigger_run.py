import requests as req


def trigger_run(
        api_key: str,
        project_token: str,
        start_url: str,
        start_template: dict =None,
        start_value_override=None,
        send_email: int=1
    ) -> dict:
    
    url = f"https://www.parsehub.com/api/v2/projects/{project_token}/run"
    params = {
        "api_key": api_key,
        "start_url": start_url,
        "start_value_override": start_value_override,
        "send_email": send_email
    }
    
    r = req.post(url, data=params)
    r.raise_for_status()
    return r