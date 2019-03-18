
from celery import shared_task

@shared_task(name="sum_numbers")
def adda():
    return 3 + 4 


@shared_task(name="helloworld")
def helloworld():
    return "Hello World from Celery" 
