from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task, Worker, Comment, TaskType, Position


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Task type name...",
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Brief description of the task type...",
                "class": "form-control",
                "rows": 3,
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = ""
        self.fields["description"].label = ""


class TaskTypeSearchForm(forms.Form):
    q = forms.CharField(
        max_length=155,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search types...",
                "class": "form-control form-control-sm",
            }
        ),
    )


class TaskForm(forms.ModelForm):
    assignee = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = ("name", "task_type", "priority", "deadline", "description", "assignee", "status")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Task Name"}),
            "description": forms.Textarea(attrs={"placeholder": "Task Description", "rows": 3}),
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ""

            if field_name != "assignee":
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({"class": "form-select"})
                elif not isinstance(field.widget, forms.DateTimeInput):
                    field.widget.attrs.update({"class": "form-control"})

        self.fields['task_type'].empty_label = "Select task type"
        self.fields['priority'].empty_label = "Select priority"
        self.fields['status'].empty_label = "Select status"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
        }

        for field_name, field in self.fields.items():
            field.label = ""

            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})

        if "position" in self.fields:
            self.fields['position'].empty_label = "Select position"


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ""
            field.widget.attrs.update({"class": "form-control"})


class WorkerSearchForm(forms.Form):
    q = forms.CharField(
        max_length=155,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search workers...",
                "class": "form-control form-control-sm",
            }
        ),
    )


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Position name...",
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Brief description of the position...",
                "class": "form-control",
                "rows": 3,
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = ""
        self.fields["description"].label = ""


class PositionSearchForm(forms.Form):
    q = forms.CharField(
        max_length=155,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search positions...",
                "class": "form-control form-control-sm",
            }
        ),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "Write comment here...",
                "class": "form-control",
                "rows": 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""