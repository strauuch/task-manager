from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tasks.models import Task, Worker, Comment


class TaskForm(forms.ModelForm):
    assignee = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "task_type",
            "priority",
            "deadline",
            "description",
            "assignee",
            "status",
        )
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }
        # fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email",
        )


class TaskTypeSearchForm(forms.Form):
    q = forms.CharField(
        max_length=155,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control",
            }
        ),
    )


class PositionSearchForm(forms.Form):
    q = forms.CharField(
        max_length=155,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "class": "form-control",
            }
        ),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment here..."}
            )
        }
