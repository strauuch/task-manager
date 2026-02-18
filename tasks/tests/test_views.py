from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

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
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123", position=self.position
        )
        self.worker = get_user_model().objects.create_user(
            username="worker_test",
            password="workerpassword",
            position=self.position,
            first_name="John",
            last_name="Doe",
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            status=Status.PENDING,
            priority=Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignee.add(self.worker)
        self.client.login(username="test_user", password="password123")


class IndexViewTests(BaseViewTestCase):
    def test_index_logic_and_template(self):
        self.client.login(username="worker_test", password="workerpassword")

        Task.objects.create(
            name="Completed Task",
            description="...",
            status=Status.COMPLETED,
            task_type=self.task_type,
        ).assignee.add(self.worker)

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertEqual(len(response.context["active_tasks"]), 1)
        self.assertEqual(response.context["active_tasks"][0].status, Status.PENDING)


class TaskTypeViewsTests(BaseViewTestCase):
    def test_task_type_detail_and_template(self):
        response = self.client.get(
            reverse("task-type-detail", kwargs={"pk": self.task_type.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_type_detail.html")

    def test_task_type_update_and_delete(self):
        self.client.post(
            reverse("task-type-update", kwargs={"pk": self.task_type.pk}),
            {"name": "Updated"},
        )
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Updated")

        response = self.client.post(
            reverse("task-type-delete", kwargs={"pk": self.task_type.pk})
        )
        self.assertRedirects(response, reverse("task-type-list"))
        self.assertFalse(TaskType.objects.filter(pk=self.task_type.pk).exists())


class TaskViewsTests(BaseViewTestCase):
    def test_task_pagination_and_filters(self):
        for i in range(15):
            Task.objects.create(
                name=f"Task {i}", description="...", task_type=self.task_type
            )

        response = self.client.get(reverse("task-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["tasks"]), 10)

        response_filter = self.client.get(reverse("task-list"), {"priority": "high"})
        self.assertTrue(
            all(t.priority == "high" for t in response_filter.context["tasks"])
        )

    def test_task_update_and_delete(self):
        payload = {
            "name": "Edited",
            "description": "New desc",
            "status": "in_progress",
            "priority": "low",
            "task_type": self.task_type.pk,
            "assignee": [self.worker.pk],
        }
        self.client.post(reverse("task-update", kwargs={"pk": self.task.pk}), payload)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Edited")

        self.client.post(reverse("task-delete", kwargs={"pk": self.task.pk}))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class WorkerViewsTests(BaseViewTestCase):
    def test_worker_detail_and_template(self):
        response = self.client.get(
            reverse("worker-detail", kwargs={"pk": self.worker.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")

    def test_worker_create_view_post(self):
        payload = {
            "username": "new_worker",
            "email": "new_worker@test.com",
            "password1": "paSsword_123",
            "password2": "paSsword_123",
            "first_name": "New",
            "last_name": "Worker",
            "position": self.position.pk,
        }
        response = self.client.post(reverse("worker-create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="new_worker").exists())

    def test_worker_update_and_delete(self):
        payload = {
            "username": "updated_worker",
            "first_name": "New",
            "last_name": "Name",
            "email": "test@test.com",
            "position": self.position.pk,
        }
        self.client.post(
            reverse("worker-update", kwargs={"pk": self.worker.pk}), payload
        )
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "updated_worker")

        self.client.post(reverse("worker-delete", kwargs={"pk": self.worker.pk}))
        self.assertFalse(get_user_model().objects.filter(pk=self.worker.pk).exists())


class PositionViewsTests(BaseViewTestCase):
    def test_position_detail_and_template(self):
        response = self.client.get(
            reverse("position-detail", kwargs={"pk": self.position.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_detail.html")

    def test_position_create_view_post(self):
        payload = {"name": "Designer", "description": "UI/UX design"}
        response = self.client.post(reverse("position-create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Designer").exists())

    def test_position_update_and_delete(self):
        self.client.post(
            reverse("position-update", kwargs={"pk": self.position.pk}),
            {"name": "Lead"},
        )
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Lead")

        self.client.post(reverse("position-delete", kwargs={"pk": self.position.pk}))
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())


class CommentViewsTests(BaseViewTestCase):
    def test_comment_delete_and_redirect(self):
        comment = Comment.objects.create(
            task=self.task, author=self.user, content="To be deleted"
        )
        response = self.client.post(
            reverse("comment-delete", kwargs={"pk": comment.pk})
        )
        self.assertRedirects(response, self.task.get_absolute_url())
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_comment_update_hacks_prevention(self):
        other_user = get_user_model().objects.create_user(
            username="other", password="123"
        )
        other_comment = Comment.objects.create(
            task=self.task, author=other_user, content="No touch"
        )

        response = self.client.post(
            reverse("comment-update", kwargs={"pk": other_comment.pk}),
            {"content": "Hacked"},
        )
        self.assertEqual(response.status_code, 404)
        other_comment.refresh_from_db()
        self.assertEqual(other_comment.content, "No touch")

    def test_add_comment_via_task_detail_post(self):
        # Testing the 'post' method in TaskDetailView for comment creation
        comment_content = "This is a test comment from DetailView"
        response = self.client.post(
            reverse("task-detail", kwargs={"pk": self.task.pk}),
            data={"content": comment_content},
        )

        self.assertRedirects(
            response, reverse("task-detail", kwargs={"pk": self.task.pk})
        )

        new_comment = Comment.objects.get(content=comment_content)
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.task, self.task)
