from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta


from materials.models import Subscription
from users.models import User


@shared_task
def send_course_update_email(course_id):
    """Отправляет сообщение об обновлении курса"""
    subscriptions = Subscription.objects.filter(course_id=course_id)

    emails = [sub.user.email for sub in subscriptions if sub.user.email]

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


@shared_task
def deactivate_inactive_users():
    """Деактивирует пользователей, которые не заходили более 30 дней"""
    threshold_date = timezone.now() - timedelta(days=30)

    users = User.objects.filter(last_login__lt=threshold_date, is_active=True)

    count = users.update(is_active=False)

    return f"Деактивировано {count} пользователей"
