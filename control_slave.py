from sqlalchemy import and_

from app import create_app
from app.models import Run, RunStatus, Meta
from utils import control_vm_state, get_user_metadata


def main() -> None:
    app = create_app()
    db = app.extensions["sqlalchemy"]
    with app.app_context(), db.session.begin():
        NUM_SLAVES = get_user_metadata(Meta.NUM_SLAVES)
        for i in range(NUM_SLAVES):
            slave_name = f"slave{i+1}"
            active_run = db.session.query(Run).exists().filter(
                and_(
                    Run.slave == slave_name,
                    Run.status.in_([
                        RunStatus.WAITING,
                        RunStatus.QUEUED,
                        RunStatus.INITIALIZED,
                        RunStatus.RUNNING
                    ])
                )
            ).scalar()
            
            action = "start" if active_run else "stop"
            
            try:
                control_vm_state(vm_name=slave_name, action=action)
            except Exception as e:
                print(f"Error occured when trying to {action} {slave_name}: {e}")
            
            
if __name__ == "__main__":
    main()
            