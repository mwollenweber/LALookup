import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LALookup.settings')

app = Celery('LALookup')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'UTC'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': 'test',
        'schedule': 10.0,
    },
    'loadLegislators': {
        'task': 'loadLegislators',
        'schedule': 60.0,
    },
}