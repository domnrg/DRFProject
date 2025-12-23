from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        required=False, validators=[YoutubeLinkValidator()]
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "course",
            "description",
            "video_url",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"


class LessonDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.course).count()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "course",
            "description",
            "video_url",
            "lessons_count",
        )
