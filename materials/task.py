from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

@shared_task
def send_update_info(email):
    send_mail('Обновление курса', 'Материалы курса были обновлены', EMAIL_HOST_USER, [email])
