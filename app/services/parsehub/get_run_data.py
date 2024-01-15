import requests as req


def get_run_data(api_key: str, run_token: str, data_format: str='json') -> dict:
    url = f"https://www.parsehub.com/api/v2/runs/{run_token}/data"
    params = {"api_key": api_key, "format": data_format}

    r = req.get(url, params=params)
    r.raise_for_status()
    return r.json()