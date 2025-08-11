import django_filters
from django.db.models import Q
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

    q = django_filters.CharFilter(method='filter_search', label='Search')
    task_type = django_filters.ModelChoiceFilter(queryset=TaskType.objects.all(), label='Type')
    assignee = django_filters.ModelChoiceFilter(queryset=Worker.objects.all(), label='Assignee')
    priority = django_filters.ChoiceFilter(choices=Task._meta.get_field('priority').choices)
    status = django_filters.ChoiceFilter(choices=Task._meta.get_field('status').choices)
    deadline = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )
    active_filter = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES, method="filter_active", empty_label=None, label="Show", initial=STATUS_ACTIVE,
    )

    class Meta:
        model = Task
        fields = ["task_type", "assignee", "priority", "status", "active_filter"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(task_type__name__icontains=value)
        ).distinct()

    def filter_active(self, queryset, name, value):
        if value == self.STATUS_ACTIVE:
            return queryset.exclude(status__in=["canceled", "completed", "blocked"])
        if value == self.STATUS_OFF:
            return queryset.filter(status__in=["canceled", "completed", "blocked"])
        return queryset
