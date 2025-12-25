from pygments.lexer import default
from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonDetailSerializer,
    LessonSerializer,
)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):

        if self.action == "create":
            # создавать могут только НЕ модераторы
            self.permission_classes = [IsAuthenticated, ~IsModerator]

        elif self.action in ["update", "partial_update"]:
            # модератор ИЛИ владелец
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ["retrieve", "list"]:
            # любой авторизованный
            self.permission_classes = [IsAuthenticated]

        elif self.action == "destroy":
            # только владелец
            self.permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    @action(detail=True, methods=("post", ))
    def send_mail(self, request, pk):
        course=get_object_or_404(Course,pk=pk)




class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(Course, id=course_id)

        subs_qs = Subscription.objects.filter(user=user, course=course)

        if subs_qs.exists():
            subs_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
