from celery import shared_task
import time
import datetime
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_acknowledgement_email(task):
    logger.info("Sending acknowledgement email...")
    send_mail(
        task.task_name,
        task.task_description,
        '19131a05r0@gvpce.ac.in',
        ['gowthamkumarvulluri@gmail.com'],
        fail_silently=False,
    )
    logger.info("Email sent at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    

@shared_task
def add(x, y):
    print("getting task info")
    time.sleep(10)
    print("processed task...")
    return x + y