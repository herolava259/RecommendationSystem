from celery import Celery
from api.infrastructures.emails.mail import mail, create_message
from typing import List, Tuple
from asgiref.sync import async_to_sync

c_app = Celery()

c_app.config_from_object("src.config")

@c_app.task()
def send_email(recipients: List[Tuple[str, str]], subject: str, body: str):

    message = create_message(recipients, subject, body)
    async_to_sync(mail.send_message)(message)

    print("Email sent")