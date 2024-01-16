from google.auth import default
from googleapiclient import discovery
import requests as req

from .user_metadata import MetaUrl, HEADER_GG_METADATA

def get_vm_ext_ip(instance: str) -> str:
    """
    Retrieve the external IP address of a specified instance in the same project and zone using the default authentication on Google Cloud Platform (GCP).

    Parameters:
    - instance (str): The name of the instance for which to retrieve the external IP address.

    Returns:
    - str: The external IP address of the specified instance.

    Raises:
    - requests.exceptions.HTTPError: If the HTTP request to the Metadata Server fails.
    - googleapiclient.errors.HttpError: If there is an error in the Google Cloud API request.

    Note:
    This function assumes the specified instance is in the same project and zone as the service account used for authentication.

    Example:
    >>> get_master_ext_ip('my-instance-name')
    '123.456.789.012'
    """
    credentials, project_id = default()
    zone = req.get(MetaUrl.ZONE.value, header=HEADER_GG_METADATA).split("/")[-1]

    compute = discovery.build('compute', 'v1', credentials=credentials)
    instance_info = compute.instances().get(project=project_id, zone=zone, instance=instance).execute()
    external_ip = instance_info['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    return external_ip
