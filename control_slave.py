from sqlalchemy import or_, and_

from .app import create_app
from .app.models.Run import Run
from .utils.vm_metadata_extraction import get_vm_meta
from .utils.init import run_ps_cmd


def control_slave(action, slave_name,zone: str = "australia-southeast1-b"):
        cmd = ["gcloud", "compute", "instances", action, slave_name, f"--zone={zone}"]
        run_ps_cmd(cmd)
    
def main(zone: str = "australia-southeast1-b"):
    app = create_app()
    num_slaves = get_vm_meta("num_slaves")
    for i in range(num_slaves):
        # status require starting: waiting, queue, initialized, running,   
        # status require stopping: completed, cancelled, unknown_error, new_run_token_not_found  
        active_run = Run.query.filter(
            and_(
                Run.slave == f"slave{i+1}",
                or_(Run.status == "waiting",
                    Run.status == "queue",
                    Run.status == "initialized",
                    Run.status == "running")
            )
        ).first()
        
        if active_run:
            action = "start"
        else:
            action = "stop"
            
        cmd = ["gcloud", "compute", "instances", action, f"slave{i+1}", f"--zone={zone}"]
        run_ps_cmd(cmd)
        