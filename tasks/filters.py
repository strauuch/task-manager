import django_filters
from django import forms
from django.db.models import Q
from django.utils.timezone import localdate, timedelta
from tasks.models import Task, TaskType, Worker


class TaskFilter(django_filters.FilterSet):
    STATUS_ACTIVE = "active"
    STATUS_ALL = "all"
    STATUS_OFF = "deactive"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active only"),
        (STATUS_ALL, "All tasks"),
        (STATUS_OFF, "Inactive only"),
    ]

    DEADLINE_TODAY = "today"
    DEADLINE_OVERDUE = "overdue"
    DEADLINE_TOMORROW = "tomorrow"
    DEADLINE_THIS_WEEK = "this_week"
    DEADLINE_NEXT_WEEK = "next_week"
    DEADLINE_ALL = "all"

    DEADLINE_CHOICES = [
        (DEADLINE_TODAY, "Today"),
        (DEADLINE_OVERDUE, "Overdue"),
        (DEADLINE_TOMORROW, "Tomorrow"),
        (DEADLINE_THIS_WEEK, "This week"),
        (DEADLINE_NEXT_WEEK, "Next week"),
        (DEADLINE_ALL, "All time"),
    ]

    q = django_filters.CharFilter(
        method="filter_search",
        label="Search",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Search tasks..."
        })
    )

    task_type = django_filters.ModelChoiceFilter(
        queryset=TaskType.objects.all(),
        label="Type",
        empty_label="—",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    assignee = django_filters.ModelChoiceFilter(
        queryset=Worker.objects.all(),
        label="Assignee",
        empty_label="—",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    priority = django_filters.ChoiceFilter(
        choices=Task._meta.get_field("priority").choices,
        empty_label="—",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
        )

    status = django_filters.ChoiceFilter(
        choices=Task._meta.get_field("status").choices,
        empty_label="—",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
        )

    active_filter = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method="filter_active",
        empty_label=None,
        label="Show",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    deadline_filter = django_filters.ChoiceFilter(
        choices=DEADLINE_CHOICES,
        method="filter_deadline",
        label="Deadline",
        empty_label="—",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(task_type__name__icontains=value)
        ).distinct()

    def filter_active(self, queryset, name, value):
        if not value or value == self.STATUS_ACTIVE:
            return queryset.exclude(status__in=["canceled", "completed", "blocked"])
        if value == self.STATUS_OFF:
            return queryset.filter(status__in=["canceled", "completed", "blocked"])
        if value == self.STATUS_ALL:
            return Task.objects.all()
        return queryset

    def filter_deadline(self, queryset, name, value):
        today = localdate()

        if value == self.DEADLINE_TODAY:
            return queryset.filter(deadline__date=today)
        if value == self.DEADLINE_OVERDUE:
            return queryset.filter(deadline__date__lt=today)
        if value == self.DEADLINE_TOMORROW:
            return queryset.filter(deadline__date=today + timedelta(days=1))
        if value == self.DEADLINE_THIS_WEEK:
            start = today
            end = today + timedelta(days=6 - today.weekday())
            return queryset.filter(deadline__date__range=(start, end))
        if value == self.DEADLINE_NEXT_WEEK:
            start = today + timedelta(days=7 - today.weekday())
            end = start + timedelta(days=6)
            return queryset.filter(deadline__date__range=(start, end))
        return queryset
