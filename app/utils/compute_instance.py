from google.auth import default
from googleapiclient import discovery
import requests as req

from .user_metadata import MetaUrl, HEADER_GG_METADATA


class ComputeInstance():
    def __init__(self, instance: str):
        self.instance = instance
        self.credentials, self.project_id = default()
        self.zone = self.get_zone()
        self.compute = self.get_compute_instance()
        self.ext_ip = self.get_ext_ip()
    
    def get_zone(self) -> str:
        return req.get(MetaUrl.ZONE.value, headers=HEADER_GG_METADATA).text.split("/")[-1]
    
    def get_compute_instance(self):
        return discovery.build('compute', 'v1', credentials=self.credentials)
        
    def get_ext_ip(self) -> str:
        instance_info = self.compute.instances().get(project=self.project_id, zone=self.zone, instance=self.instance).execute()
        external_ip = instance_info['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        return external_ip
    
    def control(self, action: str)-> None:
        if action.lower() == 'start':
            self.compute.instances().start(project=self.project_id, zone=self.zone, instance=self.instance).execute()
        elif action.lower() == 'stop':
            self.compute.instances().stop(project=self.project_id, zone=self.zone, instance=self.instance).execute()
        else:
            raise ValueError("Invalid input for 'action'. Must be 'start' or 'stop'")
        
  
# def get_vm_ext_ip(instance: str) -> str:
#     """
#     Retrieve the external IP address of a specified instance in the same project and zone using the default authentication on Google Cloud Platform (GCP).

#     Parameters:
#     - instance (str): The name of the instance for which to retrieve the external IP address.

#     Returns:
#     - str: The external IP address of the specified instance.

#     Raises:
#     - requests.exceptions.HTTPError: If the HTTP request to the Metadata Server fails.
#     - googleapiclient.errors.HttpError: If there is an error in the Google Cloud API request.

#     Note:
#     This function assumes the specified instance is in the same project and zone as the service account used for authentication.

#     Example:
#     >>> get_master_ext_ip('my-instance-name')
#     '123.456.789.012'
#     """
#     credentials, project_id = default()
#     zone = req.get(MetaUrl.ZONE.value, headers=HEADER_GG_METADATA).text.split("/")[-1]

#     compute = discovery.build('compute', 'v1', credentials=credentials)
#     instance_info = compute.instances().get(project=project_id, zone=zone, instance=instance).execute()
#     external_ip = instance_info['networkInterfaces'][0]['accessConfigs'][0]['natIP']
#     return external_ip
      

# def control_vm_state(instance: str, action: str) -> None:
#     """
#     Control the state of a Virtual Machine (VM) in the same project and zone using the default authentication on Google Cloud Platform (GCP).

#     Parameters:
#     - vm_name (str): The name of the VM whose state is to be controlled.
#     - action (str): The action to be performed on the VM. Must be 'start' or 'stop'.

#     Returns:
#     - None

#     Raises:
#     - ValueError: If the 'action' parameter is not 'start' or 'stop'.

#     Example:
#     >>> control_vm_state('my-vm-instance', 'start')
#     # The specified VM instance is started.

#     >>> control_vm_state('my-vm-instance', 'stop')
#     # The specified VM instance is stopped.
#     """
#     credentials, project_id = default()
#     zone = req.get(MetaUrl.ZONE.value, headers=HEADER_GG_METADATA).text.split("/")[-1]
#     compute = discovery.build('compute', 'v1', credentials=credentials)

#     if action == 'start':
#         compute.instances().start(project=project_id, zone=zone, instance=instance).execute()
#     elif action == 'stop':
#         compute.instances().stop(project=project_id, zone=zone, instance=instance).execute()
#     else:
#         raise ValueError("Invalid input for 'action'. Must be 'start' or 'stop'")
