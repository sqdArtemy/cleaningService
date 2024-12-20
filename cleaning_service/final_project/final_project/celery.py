from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# Set default django settings as settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings.settings')

app = Celery('final_project')  # Instance of a celery
app.conf.enable_utc = True

# Adjusting celery configurations
app.conf.update(timezone='UTC')
app.config_from_object(settings, namespace='CELERY')
app.conf.update(CELERY_TASK_RESULT_EXPIRES=3600,)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
