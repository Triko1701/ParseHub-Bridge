import subprocess

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
    # subprocess.run(["gunicorn", "-b", "0.0.0.0:5000", "-w", "5", "app:app"])