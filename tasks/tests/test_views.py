from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from tasks.models import (
    Task,
    TaskType,
    Worker,
    Position,
    Comment,
    Status,
    Priority,
)


class BaseViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass12345"
        )

        self.position = Position.objects.create(name="Developer")

        self.worker = Worker.objects.create_user(
            username="worker",
            password="workerpass",
            position=self.position,
        )

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timezone.timedelta(days=1),
            status=Status.PENDING,
            priority=Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignee.add(self.worker)

    def login(self):
        self.client.login(username="user", password="pass12345")


class IndexViewTests(BaseViewTestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_index_view_context(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 2)
        self.assertEqual(response.context["num_active_tasks"], 1)


class TaskTypeViewsTests(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_task_type_list_view(self):
        response = self.client.get(reverse("task-types-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_task_type_list_search(self):
        response = self.client.get(
            reverse("task-types-list"),
            {"q": "Bug"}
        )
        self.assertContains(response, "Bug")

    def test_task_type_create(self):
        response = self.client.post(
            reverse("task-type-create"),
            data={"name": "Feature"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TaskType.objects.filter(name="Feature").exists())

    def test_task_type_update(self):
        response = self.client.post(
            reverse("task-type-update", kwargs={"pk": self.task_type.pk}),
            data={"name": "Updated"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Updated")

    def test_task_type_delete(self):
        response = self.client.post(
            reverse("task-type-delete", kwargs={"pk": self.task_type.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TaskType.objects.filter(pk=self.task_type.pk).exists())


class TaskViewsTests(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_list_context(self):
        response = self.client.get(reverse("tasks-list"))
        self.assertIn("filter", response.context)
        self.assertIn("today", response.context)

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("task-detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.description)

    def test_task_detail_404(self):
        response = self.client.get(
            reverse("task-detail", kwargs={"pk": 999})
        )
        self.assertEqual(response.status_code, 404)

    def test_task_create_view(self):
        response = self.client.post(
            reverse("task-create"),
            {
                "name": "New task",
                "description": "Desc",
                "deadline": timezone.now() + timezone.timedelta(days=2),
                "status": Status.PENDING,
                "priority": Priority.LOW,
                "task_type": self.task_type.pk,
                "assignee": [self.worker.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New task").exists())

    def test_task_update_view(self):
        response = self.client.post(
            reverse("task-update", kwargs={"pk": self.task.pk}),
            {
                "name": "Updated task",
                "description": self.task.description,
                "deadline": self.task.deadline,
                "status": self.task.status,
                "priority": self.task.priority,
                "task_type": self.task.task_type.pk,
                "assignee": [self.worker.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated task")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("task-delete", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class WorkerAndPositionViewsTests(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_worker_list(self):
        response = self.client.get(reverse("workers-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.username)

    def test_worker_detail(self):
        response = self.client.get(
            reverse("worker-detail", kwargs={"pk": self.worker.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_position_list(self):
        response = self.client.get(reverse("positions-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_position_search(self):
        response = self.client.get(
            reverse("positions-list"),
            {"q": "Dev"}
        )
        self.assertContains(response, "Developer")


class CommentViewsTests(BaseViewTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_add_comment(self):
        response = self.client.post(
            reverse("task-detail", kwargs={"pk": self.task.pk}),
            {"content": "Comment text"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="Comment text").exists())

    def test_update_comment(self):
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="Old",
        )
        response = self.client.post(
            reverse("comment-update", kwargs={"pk": comment.pk}),
            {"content": "New"},
        )
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, "New")

    def test_delete_comment(self):
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="Delete me",
        )
        response = self.client.post(
            reverse("comment-delete", kwargs={"pk": comment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
