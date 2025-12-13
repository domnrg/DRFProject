from django.core.management.base import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создать тестовые платежи"

    def handle(self, *args, **options):
        # Получаем пользователя
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.WARNING("Нет пользователей для привязки"))
            return

        # Получаем курс и урок
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not course and not lesson:
            self.stdout.write(self.style.WARNING("Нет курса или урока для привязки"))
            return

        # Создаём платеж
        payment = Payment.objects.create(
            user=user,
            paid_course=course,
            paid_lesson=lesson,
            amount=1000,
            method="cash",
            date=timezone.now(),
        )

        self.stdout.write(self.style.SUCCESS(f"Платеж {payment.id} создан"))
