from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment, User
from .permissions import IsModerator
from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_payment


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "method")
    ordering_fields = ["date"]
    ordering = ["-date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(
            user=self.request.user, method="stripe", status="pending"
        )

        course = payment.paid_course

        session_data = create_stripe_payment(
            amount=payment.amount,
            name=course.name,
        )

        payment.stripe_session_id = session_data["session_id"]
        payment.payment_link = session_data["payment_url"]
        payment.save()
