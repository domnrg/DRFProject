from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name")

class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, object):
        return Lesson.objects.filter(course=object.course).count()

    class Meta:
        model = Lesson
        fields = ("id", "name","course", "description", "lessons_count")
