from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task, Worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {"deadline": forms.DateInput(attrs={"type": "datetime-local"}),}
        fields = ("name", "task_type", "priority", "deadline", "description", "assignee", "status")
        # fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position", "email", )