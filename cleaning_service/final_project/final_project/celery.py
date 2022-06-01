from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings.settings')

app = Celery('final_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Tashkent')
app.config_from_object(settings, namespace='CELERY')


# Celery beat settings
app.conf.beat_schedule = {
    'test-task-every-10-seconds': {
        'task': 'core.tasks.test_func',
        'schedule': 10.0,
        #'args': (),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')