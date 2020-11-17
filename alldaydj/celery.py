"""
    Long Running Celery Tasks
"""

import os
from celery import Celery

# Auto configuration

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alldaydj.settings")
app = Celery("alldaydj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()