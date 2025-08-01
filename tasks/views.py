from django.shortcuts import render
from django.views import generic

from tasks.models import TaskType, Task, Worker


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
    template_name = "tasks/task_type_list.html"
    paginate_by = 10

class TaskListView(generic.ListView):
    """View class for the tasks page of the site."""

    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    paginate_by = 10