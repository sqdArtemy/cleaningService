import pytest
from core.tasks import test_func
from final_project.celery import app

pytestmark = pytest.mark.django_db  # Links with django data base

# Testing celery function
def test_celery_beat_task(celery_worker):
    result = test_func.delay()
    assert result.get() == 'Done'