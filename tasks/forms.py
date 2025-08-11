from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tasks.models import Task, Worker


class TaskForm(forms.ModelForm):
    assignee = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Task
        widgets = {"deadline": forms.DateInput(attrs={"type": "datetime-local"}),}
        fields = ("name", "task_type", "priority", "deadline", "description", "assignee", "status")
        # fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position", "email", )