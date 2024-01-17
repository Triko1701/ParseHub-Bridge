from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient import discovery
import requests as req

from .user_metadata import MetaUrl, HEADER_GG_METADATA

class ComputeInstance():
    def __init__(self, instance: str, sa_key_path: str=None, zone: str=None):
        self.instance = instance
        self.cred, self.proj_id = self.get_cred_proj_id(sa_key_path)
        self.zone = self.get_zone() if not zone else zone
        self.compute = self.get_compute_instance()
        self.info = self.get_info()
    
    def get_cred_proj_id(self, sa_key_path: str):
        if not sa_key_path:
            cred, proj_id = default()
            return cred, proj_id
        
        cred = service_account.Credentials.from_service_account_file(
            sa_key_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform'],
        )
        if cred.requires_scopes:
            cred = cred.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        return cred, cred.project_id
        
    def get_zone(self) -> str:
        return req.get(MetaUrl.ZONE.value, headers=HEADER_GG_METADATA).text.split("/")[-1]
    
    def get_compute_instance(self):
        return discovery.build('compute', 'v1', credentials=self.cred)
    
    def get_info(self):
        self.cred.refresh(Request())
        info = self.compute.instances().get(project=self.proj_id, zone=self.zone, instance=self.instance).execute()
        return info
    
    @property
    def metadata(self) -> dict:
        self.cred.refresh(Request())
        instance_info = self.compute.instances().get(project=self.proj_id, zone=self.zone, instance=self.instance).execute()
        metadata = instance_info.get('metadata', {}).get('items', [])
        metadata_dict = {item['key']: item['value'] for item in metadata}
        return metadata_dict
    
    @property
    def ext_ip(self) -> str:
        self.cred.refresh(Request())
        external_ip = self.info['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        return external_ip
    
    def control(self, action: str) -> None:
        self.cred.refresh(Request())
        if action.lower() == 'start':
            self.compute.instances().start(project=self.proj_id, zone=self.zone, instance=self.instance).execute()
        elif action.lower() == 'stop':
            self.compute.instances().stop(project=self.proj_id, zone=self.zone, instance=self.instance).execute()
        else:
            raise ValueError("Invalid input for 'action'. Must be 'start' or 'stop'")
        