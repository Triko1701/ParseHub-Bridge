import requests

def get_vm_meta_field(*fields):
    results = []
    
    # Define headers with the required Metadata-Flavor
    headers = {"Metadata-Flavor": "Google"}
    for field in fields:
        # Define the metadata URL for the VM name
        metadata_url = f"http://metadata.google.internal/computeMetadata/v1/instance/{field}"
    
        # Make a GET request to retrieve the VM name
        response = requests.get(metadata_url, headers=headers)
    
        # Check if the request was successful, print and append the result to the list
        if response.status_code == 200:
            value = response.text
            print(f"{field}: {value}")
            results.append(value)
        else:
            print(f"Failed to retrieve {field}")
            results.append(None)
    
    return tuple(results)


# def get_vm_meta_field(field):

#     # Define the metadata URL for the VM name
#     metadata_url = f"http://metadata.google.internal/computeMetadata/v1/instance/{field}"

#     # Define headers with the required Metadata-Flavor
#     headers = {"Metadata-Flavor": "Google"}

#     # Make a GET request to retrieve the VM name
#     response = requests.get(metadata_url, headers=headers)

#     # Check if the request was successful, print and return the VM name
#     if response.status_code == 200:
#         value = response.text
#         print(f"{field}: {value}")
#         return value
#     else:
#         vm_name = None
#         print(f"Failed to retrieve {field}")
#         return value