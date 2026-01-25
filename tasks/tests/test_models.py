from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from tasks.models import (
    Task,
    TaskType,
    Status,
    Priority,
    Position,
    Comment,
)


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")

        self.user = get_user_model().objects.create_user(
            username="john",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )

        self.task = Task.objects.create(
            name="Finish project",
            description="Finish Django project before deadline",
            deadline=timezone.now() + timezone.timedelta(days=1),
            status=Status.PENDING,
            priority=Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignee.add(self.user)

    def test_task_str(self):
        self.assertIn("Finish project", str(self.task))

    def test_task_has_assignee(self):
        self.assertEqual(self.task.assignee.count(), 1)
        self.assertIn(self.user, self.task.assignee.all())

    def test_task_default_status(self):
        task = Task.objects.create(
            name="Default status task",
            description="Test default status",
            task_type=self.task_type,
        )
        self.assertEqual(task.status, Status.PENDING)

    def test_task_get_absolute_url(self):
        url = self.task.get_absolute_url()
        self.assertEqual(url, reverse("task-detail", kwargs={"pk": self.task.pk}))


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.user = get_user_model().objects.create_user(
            username="alice",
            password="testpass123",
            first_name="Alice",
            last_name="Smith",
            position=self.position,
        )

    def test_worker_str_with_position(self):
        self.assertIn("Developer", str(self.user))
        self.assertIn("Alice", str(self.user))

    def test_worker_get_absolute_url(self):
        url = self.user.get_absolute_url()
        self.assertEqual(url, reverse("worker-detail", kwargs={"pk": self.user.pk}))


class CommentModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Feature")

        self.user = get_user_model().objects.create_user(
            username="bob",
            password="testpass123",
        )

        self.task = Task.objects.create(
            name="Add comments",
            description="Allow users to comment on tasks",
            task_type=self.task_type,
        )

        self.comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="Looks good to me",
        )

    def test_comment_str(self):
        self.assertIn(self.user.username, str(self.comment))
        self.assertIn(self.task.name, str(self.comment))

    def test_comment_task_relation(self):
        self.assertEqual(self.task.comments.count(), 1)
        self.assertEqual(self.task.comments.first(), self.comment)
