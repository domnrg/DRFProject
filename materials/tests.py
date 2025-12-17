from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="12345")
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_create")
        data = {
            "name": "Lesson 2",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Lesson 2",
            "course": self.course.id
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Lesson 2")

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], list)


class CourseTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="12345")
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-list")
        data = {
            "name": "New course"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data["name"], "New course")

    def test_course_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Update course",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Update course")

    def test_course_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], list)
