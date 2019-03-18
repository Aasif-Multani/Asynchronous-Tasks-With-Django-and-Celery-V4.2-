from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCeleryRedis.settings')

app = Celery('DjangoCeleryRedis')
app.conf.broker_heartbeat = 0

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from celery.schedules import crontab
# app.conf.beat_schedule = {
#     # 'add-every-minute-contrab': {
#     #     'task': 'multiply_two_numbers',
#     #     'schedule': crontab(),
#     #     'args': (16, 16),
#     # },
#     # 'add-every-5-seconds': {
#     #     'task': 'multiply_two_numbers',
#     #     'schedule': 5.0,
#     #     'args': (16, 16)
#     # },
#     'add-every-30-seconds': {
#         'task': 'add',
#         'schedule': 30.0,
#         'args': (16, 16)
#     },
# }

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
	