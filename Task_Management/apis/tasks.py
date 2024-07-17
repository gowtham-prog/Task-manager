from celery import shared_task
import time
import datetime

@shared_task
def send_acknowledgement_email():
    print("Sending acknowledgement email...")
    
    print("Email sent at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))