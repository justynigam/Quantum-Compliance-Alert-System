import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qercas_project.settings')

app = Celery('qercas_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['transactions'])

# Windows-specific settings
if os.name == 'nt':
    # Use eventlet for better Windows compatibility
    app.conf.update(
        worker_pool='solo',  # Use solo pool instead of prefork
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )

# Optional: Add periodic tasks
app.conf.beat_schedule = {
    'run-federated-learning-every-day': {
        'task': 'federated_learning.tasks.run_federated_training',
        'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
}
