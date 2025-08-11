from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {"deadline": forms.DateInput(attrs={"type": "datetime-local"}),}
        fields = ("name", "task_type", "priority", "deadline", "description", "assignee", "status")
        # fields = "__all__"