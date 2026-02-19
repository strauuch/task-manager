from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.forms import (
    TaskForm,
    WorkerCreationForm,
    PositionForm,
    WorkerSearchForm,
    CommentForm,
)
from tasks.models import Task, TaskType, Position


class FormLogicTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Development")
        self.position = Position.objects.create(name="Developer")
        self.worker1 = get_user_model().objects.create_user(
            username="w1", password="pw1"
        )
        self.worker2 = get_user_model().objects.create_user(
            username="w2", password="pw2"
        )

    def test_task_form_save_with_assignees(self):
        form_data = {
            "name": "New Task",
            "description": "Desc",
            "priority": "high",
            "status": "pending",
            "task_type": self.task_type.id,
            "assignee": [self.worker1.id, self.worker2.id],
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.assignee.count(), 2)
        self.assertIn(self.worker1, task.assignee.all())

    def test_worker_creation_password_mismatch(self):
        form_data = {
            "username": "new_user",
            "password1": "pass123",
            "password2": "different_pass",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertEqual(
            form.errors["password2"], ["The two password fields didn’t match."]
        )

    def test_position_form_save(self):
        form_data = {"name": "Manager", "description": "Team lead"}
        form = PositionForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(Position.objects.filter(name="Manager").exists())

    def test_search_form_empty_q(self):
        form = WorkerSearchForm(data={"q": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["q"], "")

    def test_task_form_optional_deadline(self):
        form_data = {
            "name": "Task without date",
            "description": "Some desc",
            "priority": "low",
            "status": "pending",
            "task_type": self.task_type.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_invalid_deadline(self):
        form_data = {
            "name": "Task",
            "deadline": "not-a-date",
            "task_type": self.task_type.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)


class WorkerCreationFormValidationTest(TestCase):
    def test_worker_creation_invalid_username(self):
        get_user_model().objects.create_user(username="existing_user", password="pw")
        form_data = {
            "username": "existing_user",
            "password1": "pass123",
            "password2": "pass123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CommentFormTest(TestCase):
    def test_comment_form_content_is_required(self):
        form = CommentForm(data={"content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_comment_form_valid_data(self):
        form = CommentForm(data={"content": "Test comment content"})
        self.assertTrue(form.is_valid())
