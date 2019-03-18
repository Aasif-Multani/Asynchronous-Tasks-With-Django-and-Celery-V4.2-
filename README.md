# Asynchronous-Tasks-With-Django-and-Celery-V4.2-



1. Download Redis

   redis server 
   
   ***Linux*** [https://redis.io/download]
                            
   ***Windows*** [https://github.com/tporadowski/redis/releases]

2. Open & Test Redis:

    open Terminal

    redis-cli ping

    $ redis-cli ping
    PONG

    Close Redis with control + c to quit

3. Install Celery + Redis in your virtualenv.

pip install celery

pip install redis

pip install django-celery-beat

pip install django-celery-results

pip freeze > requirements.txt


4. Update Django settings.py:

INSTALLED_APPS = [

    'django.contrib.admin',
    
    'django.contrib.auth',
    
    'django.contrib.contenttypes',
    
    'django.contrib.sessions',
    
    'django.contrib.messages',
    
    'django.contrib.staticfiles',
    
    'django_celery_beat',
    
    'django_celery_results',
    
]


CELERY_BROKER_URL = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = TIME_ZONE

5. Create celery.py to setup Celery app: Navigate to project config module (where settings and urls modules are) and create a celery.py file with the contents:

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

@app.task(bind=True)

def debug_task(self):

    print('Request: {0!r}'.format(self.request))

6. Update project conf folder's __init__.py file:

# DjangoCeleryRedis/__init__.py

from __future__ import absolute_import

# This will make sure the app is always imported when

# Django starts so that shared_task will use this app.

from .celery import app as celery_app  # noqa

7. Create tasks.py in your Django app (a valid app in INSTALLED_APPS):

from __future__ import absolute_import, unicode_literals

import random

from celery.decorators import task

@task(name="sum_two_numbers")

def add(x, y):

    return x + y


@task(name="multiply_two_numbers")

def mul(x, y):

    total = x * (y * random.randint(3, 100))
    
    return total


@task(name="sum_list_numbers")

def xsum(numbers):

    return sum(numbers)

8. Run migrations: python manage.py makemigrations and python manage.py migrate

9. Test tasks:

    Open a terminal window, Run Celery with in your project root where manage.py lives:

    celery -A yourproject worker -l info

    celery -A yourproject worker -l debug (for debugging)
    
    # like 
    
    celery -A cfehome worker -l info

    Open another terminal window, in your Django project python manage.py shell:

    >>> from yourapp.tasks import add, mul, xsum
    
    >>> add(1,3)
    4
    >>> add.delay(1,3)
    
    <AsyncResult: 7bb03f9a-5702-4661-b737-2bc54ed9f558>

    If you look at your celery worker, you should see something like:

    [2016-11-08 22:05:22,686: INFO/PoolWorker-5] Task sum_two_numbers[7bb03f9a-5702-4661-b737-2bc54ed9f558] succeeded in 0.0004559689841698855s: 21

Setup Schedule to Run Tasks Docs:

10. ### Known Issues and Fixes ### :

Compatibility Issue with Python 3.7 :

    Symptom :
    - File "c:\users\biswa\appdata\local\conda\conda\envs\nutri\lib\site-packages\celery\backends\redis.py", line 22
        from . import async, base
                  ^
      SyntaxError: invalid syntax

    Fix :
    
    - rename "site-packages/celery/backends/async.py" to "asynchronous.py"
    
    - modify the usages of "async" inside "site-packages/celery/backends/redis.py" and 
      "site-packages/celery/backends/rpc.py" to "asynchronous".

ValueError: not enough values to unpack (expected 3, got 0) :

    Symptom :
    
    - ValueError: not enough values to unpack (expected 3, got 0)

    Fix :
    
    - set the ENVIRONMENT_VARIABLE "FORKED_BY_MULTIPROCESSING" to 1.
    
        i.e. : in terminal run "set FORKED_BY_MULTIPROCESSING=1"
        
      (This will be a temporary environment variable. To store it as permanent, add it to windows PATH and Variable)

11. Setup Schedule to Run Tasks Docs:

# celery.py

from celery.schedules import crontab

app.conf.beat_schedule = {

    'add-every-minute-contrab': {
    
        'task': 'multiply_two_numbers',
        
        'schedule': crontab(),
        
        'args': (16, 16),
    },
    
    'add-every-5-seconds': {
    
        'task': 'multiply_two_numbers',
        
        'schedule': 5.0,
        
        'args': (16, 16)
    }
    
}

12. Test Scheduled Task with Celery Beat: open another terminal windows to run scheduled task:

    celery -A DjangoCeleryRedis beat -l info

    celery -A DjangoCeleryRedis beat -l debug (for debugging)

13. ### Known Issues and Fixes ### :

    Symptom :

    celery beat v4.2.0 (windowlicker) is starting.

    ERROR: Pidfile (celerybeat.pid) already exists.

    Seems we're already running? (pid: 12008)

    Fix :

    Remove celerybeat.pid file from your project.
