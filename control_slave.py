from sqlalchemy import or_, and_

from app import create_app
from app.models.Run import Run
from utils.metadata_extraction import get_custom_metadata
from utils.gce import control_vm_state


def main():
    num_slaves = get_custom_metadata("NUM_SLAVES")
    app = create_app()
    with app.app_context():
        for i in range(num_slaves):
            slave_name = f"slave{i+1}"
            # status require starting: waiting, queue, initialized, running,   
            active_run = Run.query.filter(
                and_(
                    Run.slave == slave_name,
                    or_(Run.status == "waiting",
                        Run.status == "queue",
                        Run.status == "initialized",
                        Run.status == "running")
                )
            ).first()
            
            action = "start" if active_run else "stop"
            control_vm_state(instance_name=slave_name, action=action)
            
            
if __name__ == "__main__":
    main()
            