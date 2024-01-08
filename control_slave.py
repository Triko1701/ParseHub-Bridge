from sqlalchemy import or_, and_

from app import create_app
from app.models.Run import Run
from utils.vm_metadata_extraction import get_vm_metadata
from utils.init import run_ps_cmd


def control_slave(action, slave_name,zone: str = "australia-southeast1-b"):
        cmd = ["gcloud", "compute", "instances", action, slave_name, f"--zone={zone}"]
        run_ps_cmd(cmd)
    
def main(zone: str = "australia-southeast1-b"):
    num_slaves = get_vm_metadata("NUM_SLAVES")
    app = create_app()
    with app.app_context():
        for i in range(num_slaves):
            # status require starting: waiting, queue, initialized, running,   
            active_run = Run.query.filter(
                and_(
                    Run.slave == f"slave{i+1}",
                    or_(Run.status == "waiting",
                        Run.status == "queue",
                        Run.status == "initialized",
                        Run.status == "running")
                )
            ).first()
            
            action = "start" if active_run else "stop"
            cmd = ["gcloud", "compute", "instances", action, f"slave{i+1}", f"--zone={zone}"]
            run_ps_cmd(cmd)
            