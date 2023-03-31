"""Celery tasks."""

from celery import Celery
import os


celery = Celery("secureblogs")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")


@celery.task(name="test_task")
def test_task(arg):
    print(f"Test task: {arg}")
    return True
