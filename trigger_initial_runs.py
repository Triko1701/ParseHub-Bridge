from app import create_app
from app.services.parsehub import trigger_waiting_runs


def main():
    app = create_app()
    with app.app_context():
        trigger_waiting_runs(n=100)

if __name__ == "__main__":
    main()