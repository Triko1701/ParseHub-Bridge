import requests


def get_custom_metadata(*keys):
    results = []
    headers = {"Metadata-Flavor": "Google"}
    for key in keys:
        metadata_url = f"http://metadata.google.internal/computeMetadata/v1/instance/attributes/{key}"
        response = requests.get(metadata_url, headers=headers)
    
        if response.status_code == 200:
            value = response.text
            print(f"{key}: {value}")
            results.append(value)
        else:
            print(f"Failed to retrieve {key}")
            results.append(None)
    
    return tuple(results)

def get_ext_ip():
    headers = {"Metadata-Flavor": "Google"}
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip"
    response = requests.get(metadata_url, headers=headers)
    
    if response.status_code == 200:
        value = response.text
        return value
    else:
        print(f"Failed to retrieve external IP: {response.status_code}")
        return None
    
def get_project_id():
    headers = {"Metadata-Flavor": "Google"}
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    response = requests.get(metadata_url, headers=headers)
    
    if response.status_code == 200:
        value = response.text
        print(f"Project ID: {value}")
        return value
    else:
        print(f"Failed to retrieve Project ID: {response.status_code}")
        return None
    
def get_zone():
    headers = {"Metadata-Flavor": "Google"}
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/zone"
    response = requests.get(metadata_url, headers=headers)
    
    if response.status_code == 200:
        value = response.text
        zone = value.split('/')[-1]
        return zone
    else:
        print(f"Failed to retrieve the zone: {response.status_code}")
        return None
