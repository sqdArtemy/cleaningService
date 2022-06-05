import pytest
from final_project.celery import app
from core.tasks import mail_sender_task

pytestmark = pytest.mark.django_db  # Links with django data base

# Testing for mail sender task
def test_celery_beat_task(celery_worker):
    result = mail_sender_task.delay(user_mails='sqd.artemy@gmail.com', header='Test header', text='Test mail text')
    assert result.get() == 'Done'
