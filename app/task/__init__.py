from celery import Celery

app_celery = Celery('tasks', broker='redis://localhost:6379/0')