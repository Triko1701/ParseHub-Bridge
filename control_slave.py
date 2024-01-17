from sqlalchemy import and_, select

from app import create_app
from app.models import Run, RunStatus, Meta
from utils import get_user_metadata, ComputeInstance


def main() -> None:
    app = create_app(role="master")
    db = app.extensions["sqlalchemy"]
    with app.app_context(), db.session.begin():
        NUM_SLAVES = int(get_user_metadata(Meta.NUM_SLAVES.value))
        for i in range(NUM_SLAVES):
            slave_name = f"slave{i+1}"
            active_run = db.session.query(select(1).filter(
                and_(
                    Run.slave == slave_name,
                    Run.status.in_([
                        RunStatus.WAITING.value,
                        RunStatus.QUEUED.value,
                        RunStatus.INITIALIZED.value,
                        RunStatus.RUNNING.value
                    ])
                )
            ).exists()).scalar()
            
            action = "start" if active_run else "stop"
            
            try:
                slave_instance = ComputeInstance(slave_name)
                slave_instance.control(action)
                # control_vm_state(vm_name=slave_name, action=action)
            except Exception as e:
                print(f"Error occured when trying to {action} {slave_name}: {e}")
            
            
if __name__ == "__main__":
    main()
            