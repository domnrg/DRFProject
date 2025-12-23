from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "paid_course",
            "amount",
            "status",
            "method",
            "stripe_session_id",
            "payment_link",
            "created_at",
        )
        read_only_fields = (
            "status",
            "method",
            "stripe_session_id",
            "link",
            "created_at",
        )

    def get_course(self, object):
        return object.paid_course.name if object.paid_course else None

    def get_lesson(self, object):
        return object.paid_lesson.name if object.paid_lesson else None


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
