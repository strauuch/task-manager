from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=155)

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class Task(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True, default=None)
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.LOW
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    assignee = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["deadline"]

    def __str__(self):
        return (
            f"Task {self.name}, priority: {self.priority}, deadline: {self.deadline},"
        )

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=155)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.position.name if self.position else ''} {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("worker-detail", kwargs={"pk": self.pk})
