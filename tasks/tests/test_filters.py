from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, TaskType, Worker, Status, Priority
from tasks.filters import TaskFilter

class TaskFilterTest(TestCase):
    def setUp(self):
        self.type_dev = TaskType.objects.create(name="Development")
        self.type_bug = TaskType.objects.create(name="Bug")

        self.worker_john = Worker.objects.create_user(username="john_doe")

        today = timezone.localdate()

        self.task_today = Task.objects.create(
            name="Today Task",
            description="Fix something today",
            status=Status.IN_PROGRESS,
            priority=Priority.HIGH,
            task_type=self.type_dev,
            deadline=today
        )
        self.task_today.assignee.add(self.worker_john)

        self.task_overdue = Task.objects.create(
            name="Old Task",
            description="Should have been done",
            status=Status.COMPLETED,
            priority=Priority.LOW,
            task_type=self.type_bug,
            deadline=today - timedelta(days=1)
        )

        self.task_tomorrow = Task.objects.create(
            name="Future Task",
            description="Plans for tomorrow",
            status=Status.PENDING,
            task_type=self.type_dev,
            deadline=today + timedelta(days=1)
        )

    def test_filter_search_logic(self):
        qs = TaskFilter(data={'q': 'Today'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_today, qs)
        self.assertEqual(qs.count(), 1)

        qs = TaskFilter(data={'q': 'john_doe'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_today, qs)

    def test_filter_search_distinct(self):
        worker2 = get_user_model().objects.create_user(username="worker2")
        self.task_today.assignee.add(worker2)

        qs = TaskFilter(data={'q': 'Today'}, queryset=Task.objects.all()).qs
        self.assertEqual(qs.count(), 1)

    def test_filter_active_logic(self):
        qs = TaskFilter(data={'active_filter': 'active'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_today, qs)
        self.assertIn(self.task_tomorrow, qs)
        self.assertNotIn(self.task_overdue, qs)

        qs = TaskFilter(data={'active_filter': 'deactive'}, queryset=Task.objects.all()).qs
        self.assertEqual(qs.count(), 1)
        self.assertIn(self.task_overdue, qs)

    def test_filter_deadline_dates(self):
        qs = TaskFilter(data={'deadline_filter': 'today'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_today, qs)
        self.assertEqual(qs.count(), 1)

        qs = TaskFilter(data={'deadline_filter': 'overdue'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_overdue, qs)

        qs = TaskFilter(data={'deadline_filter': 'tomorrow'}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_tomorrow, qs)

    def test_filter_this_week_logic(self):
        today = timezone.localdate()
        days_until_sunday = 6 - today.weekday()

        if days_until_sunday >= 2:
            sunday_task = Task.objects.create(
                name="Sunday Task",
                task_type=self.type_dev,
                deadline=today + timedelta(days=days_until_sunday)
            )
            qs = TaskFilter(data={'deadline_filter': 'this_week'}, queryset=Task.objects.all()).qs
            self.assertIn(sunday_task, qs)

    def test_filter_by_direct_fields(self):
        qs = TaskFilter(data={'priority': Priority.HIGH}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_today, qs)
        self.assertEqual(qs.count(), 1)

        qs = TaskFilter(data={'task_type': self.type_bug.id}, queryset=Task.objects.all()).qs
        self.assertIn(self.task_overdue, qs)