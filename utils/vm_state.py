from google.auth import default
from googleapiclient import discovery
import requests as req

from .user_metadata import MetaUrl, HEADER_GG_METADATA


def control_vm_state(vm_name: str, action: str) -> None:
    """
    Control the state of a Virtual Machine (VM) in the same project and zone using the default authentication on Google Cloud Platform (GCP).

    Parameters:
    - vm_name (str): The name of the VM whose state is to be controlled.
    - action (str): The action to be performed on the VM. Must be 'start' or 'stop'.

    Returns:
    - None

    Raises:
    - ValueError: If the 'action' parameter is not 'start' or 'stop'.

    Example:
    >>> control_vm_state('my-vm-instance', 'start')
    # The specified VM instance is started.

    >>> control_vm_state('my-vm-instance', 'stop')
    # The specified VM instance is stopped.
    """
    credentials, project_id = default()
    zone = req.get(MetaUrl.ZONE, HEADER_GG_METADATA).split("/")[-1]
    compute = discovery.build('compute', 'v1', credentials=credentials)

    if action == 'start':
        compute.instances().start(project=project_id, zone=zone, instance=vm_name).execute()
    elif action == 'stop':
        compute.instances().stop(project=project_id, zone=zone, instance=vm_name).execute()
    else:
        raise ValueError("Invalid input for 'action'. Must be 'start' or 'stop'")
