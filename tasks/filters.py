from django.db.models import Q
import django_filters
from tasks.models import Task, TaskType, Worker

class TaskFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_search', label='Search')
    task_type = django_filters.ModelChoiceFilter(queryset=TaskType.objects.all(), label='Type')
    assignee = django_filters.ModelChoiceFilter(queryset=Worker.objects.all(), label='Assignee')
    priority = django_filters.ChoiceFilter(choices=Task._meta.get_field('priority').choices)
    status = django_filters.ChoiceFilter(choices=Task._meta.get_field('status').choices)
    deadline = django_filters.DateFromToRangeFilter(
        field_name='deadline',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Task
        fields = ['task_type', 'assignee', 'priority', 'status']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(task_type__name__icontains=value)
        ).distinct()
