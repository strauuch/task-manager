from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task-type-detail", kwargs={"pk": self.pk})


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    PAUSED = "paused", "Paused"
    CANCELED = "canceled", "Canceled"
    COMPLETED = "completed", "Completed"
    REVIEWING = "reviewing", "Reviewing"
    BLOCKED = "blocked", "Blocked"


class Task(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True, default=None)
    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.PENDING
    )
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

    def __str__(self):
        if self.deadline:
            return f"Task {self.name}, priority: {self.priority}, deadline: {self.deadline}"
        else:
            return f"Task {self.name}, priority: {self.priority}"

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    @property
    def time_left(self):
        if not self.deadline:
            return None

        delta = self.deadline - now()

        if delta.total_seconds() <= 0:
            return None

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")

        return " ".join(parts) if parts else "0m"


class Position(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("position-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        if self.position:
            return f"{self.username} ({self.position.name} {self.first_name} {self.last_name})"
        elif self.first_name and self.last_name:
            return f"{self.username} ({self.first_name} {self.last_name})"
        else:
            return f"{self.username}"

    def get_absolute_url(self):
        return reverse("worker-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="worker_comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.name}"
