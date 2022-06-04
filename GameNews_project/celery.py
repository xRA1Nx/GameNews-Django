import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameNews_project.settings')

app = Celery('GameNews_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_week_notify': {
        'task': 'GameNewsApp.tasks.celery_every_week_notify',
        'schedule': crontab(hour=10, minute=0, day_of_week='monday'),
        'args': (),
    },
    'printer': {
        'task': 'GameNewsApp.tasks.printer',
        'schedule': 10,
        'args': (5,)
    },

}
