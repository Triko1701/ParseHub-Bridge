from google.auth import default
from googleapiclient import discovery

from metadata_extraction import get_zone


def get_db_ip():
    credentials, project_id = default()
    zone = get_zone()
    vm_name = "master"
    compute = discovery.build('compute', 'v1', credentials=credentials)

    try:
        instance = compute.instances().get(project=project_id, zone=zone, instance=vm_name).execute()
        network_interface = instance['networkInterfaces'][0]
        access_config = network_interface['accessConfigs'][0]
        external_ip = access_config['natIP']
        return external_ip
    except Exception as e:
        print(f"Error retrieving DB IP: {e}")
        return None


def control_vm_state(instance_name, action):
    credentials, project_id = default()
    zone = get_zone()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    try:
        if action == 'start':
            request = compute.instances().start(project=project_id, zone=zone, instance=instance_name)
            response = request.execute()
            print(f"VM '{instance_name}' in project '{project_id}' started.")
        elif action == 'stop':
            request = compute.instances().stop(project=project_id, zone=zone, instance=instance_name)
            response = request.execute()
            print(f"VM '{instance_name}' in project '{project_id}' stopped.")
        else:
            print("Invalid action. Use 'start' or 'stop'.")

    except Exception as e:
        print(f"Error performing action: {e}")








