from celery import shared_task
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправляет сообщение об обновлении курса"""
    subscriptions = Subscription.objects.filter(course_id=course_id)

    emails = [
        sub.user.email
        for sub in subscriptions
        if sub.user.email
    ]

    if not emails:
        return "Нет подписчиков"

    send_mail(
        subject="Обновление курса",
        message="В курсе, на который вы подписаны, обновились материалы.",
        from_email=None,
        recipient_list=emails,
        fail_silently=False,
    )

    return f"Отправлено {len(emails)} писем"



