from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig

from .views import (
    PaymentListAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    PaymentCreateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    # пользователи
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
    # регистрация и аутентификация
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    # платежи
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/stripe/", PaymentCreateAPIView.as_view(), name="payments_stripe"),
]
