import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qercas_project.settings')

app = Celery('qercas_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicitly include the transactions app for task discovery
app.autodiscover_tasks(['transactions'])
