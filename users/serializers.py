from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "paid_course",
            "paid_lesson",
            "amount",
            "method",
            "date",
            "course",
            "lesson",
        )

    def get_course(self, object):
        return object.paid_course.name if object.paid_course else None

    def get_lesson(self, object):
        return object.paid_lesson.name if object.paid_lesson else None
