from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tasks.models import TaskType, Task, Worker, Position


def index(request):
    """View function for the home page of the site."""

    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }

    return render(request, "tasks/index.html", context=context)


class TaskTypeListView(generic.ListView):
    """View class for the task types page of the site."""

    model = TaskType
    context_object_name = "task_types"
    template_name = "tasks/task_types_list.html"
    paginate_by = 10

class TaskListView(generic.ListView):
    """View class for the tasks page of the site."""

    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.select_related("task_type")


class TaskDetailView(generic.DetailView):
    """View class for the task detail page of the site."""
    model = Task

class TaskCreateView(generic.CreateView):
    """View class for the task create page of the site."""
    # form_class = TaskForm
    model = Task
    fields = ("name", "task_type", "priority", "deadline", "description", "assignee", "status")
    success_url = reverse_lazy("tasks-list")
    template_name = "tasks/task_form.html"

class WorkerListView(generic.ListView):
    """View class for the workers page of the site."""

    model = Worker
    context_object_name = "workers"
    template_name = "tasks/workers_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Worker.objects.select_related("position")


class WorkerDetailView(generic.DetailView):
    """View class for the worker detail page of the site."""
    model = Worker


class PositionListView(generic.ListView):
    """View class for the positions page of the site."""

    model = Position
    context_object_name = "positions"
    template_name = "tasks/positions_list.html"
    paginate_by = 10