import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cts_valentine.settings")
app = Celery("cts_valentine")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()