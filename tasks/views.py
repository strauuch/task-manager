from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.db.models import Q

from tasks.filters import TaskFilter
from tasks.forms import (
    TaskForm,
    WorkerCreationForm,
    TaskTypeSearchForm,
    PositionSearchForm,
    CommentForm, TaskTypeForm, WorkerForm, WorkerSearchForm, PositionForm,
)
from tasks.models import TaskType, Task, Worker, Position, Comment


class SearchListViewMixin:
    """Mixin for ListView to provide simple search functionality by 'name' field."""

    search_form_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = self.search_form_class(self.request.GET)

        if self.form.is_valid():
            q = self.form.cleaned_data.get("q")
            if q:
                return queryset.filter(name__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context

class IndexView(LoginRequiredMixin, TemplateView):
    """Home page view that displays tasks assigned to the current user with active statuses."""

    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_statuses = [
                "pending",
                "in_progress",
                "paused",
                "reviewing",
            ]

        tasks = (
            Task.objects
            .filter(status__in=active_statuses, assignee=self.request.user)
            .select_related("task_type")
            .prefetch_related("assignee")
            .order_by("deadline")
        )
        context["active_tasks"] = tasks
        return context


class TaskTypeListView(LoginRequiredMixin, SearchListViewMixin, generic.ListView):
    """Displays a paginated list of task types with a search form."""

    model = TaskType
    context_object_name = "task_types"
    template_name = "tasks/task_type_list.html"
    paginate_by = 10
    search_form_class = TaskTypeSearchForm


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays details of a specific task type."""

    model = TaskType
    context_object_name = "task_type"
    template_name = "tasks/task_type_detail.html"



class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    """Provides a form to create a new task type."""

    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task-type-list")
    template_name = "tasks/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Provides a form to update an existing task type."""

    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task-type-list")
    template_name = "tasks/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Confirmation page and logic for deleting a task type."""

    context_object_name = "task_type"
    model = TaskType
    success_url = reverse_lazy("task-type-list")
    template_name = "tasks/task_type_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    """Displays a list of all tasks with advanced filtering by status and priority."""

    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related("assignee")
        data = self.request.GET.copy()
        if not data:
            data['active_filter'] = 'active'
        self.filterset = TaskFilter(data, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays task details and handles adding new comments via POST request."""

    model = Task
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["comments"] = task.comments.select_related("author")
        if "comment_form" not in context:
            context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect("task-detail", pk=task.pk)
        context = self.get_context_data()
        return self.render_to_response(context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Provides a form to create a new task."""

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-list")
    template_name = "tasks/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Provides a form to update an existing task."""

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-list")
    template_name = "tasks/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Confirmation page and logic for deleting a task."""

    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task-list")
    template_name = "tasks/task_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """Displays a list of workers with search by username, first name, and last name."""

    model = Worker
    context_object_name = "workers"
    template_name = "tasks/worker_list.html"
    paginate_by = 10
    search_form_class = WorkerSearchForm

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays the profile of a specific worker."""

    model = Worker
    context_object_name = "worker"
    template_name = "tasks/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles new worker registration using a custom UserCreationForm."""

    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("worker-list")
    template_name = "tasks/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Provides a form for workers or admins to update user profile information."""

    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("worker-list")
    template_name = "tasks/worker_form.html"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Confirmation page and logic for deleting a worker account."""

    model = Worker
    context_object_name = "worker"
    success_url = reverse_lazy("worker-list")
    template_name = "tasks/worker_confirm_delete.html"

class PositionListView(LoginRequiredMixin, SearchListViewMixin, generic.ListView):
    """Displays a paginated list of positions with search functionality."""

    model = Position
    context_object_name = "positions"
    template_name = "tasks/position_list.html"
    paginate_by = 10
    search_form_class = PositionSearchForm

class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays details of a specific position."""

    model = Position
    context_object_name = "position"
    template_name = "tasks/position_detail.html"

class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    """Provides a form to create a new position."""

    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("position-list")
    template_name = "tasks/position_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Provides a form to update an existing position."""

    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("position-list")
    template_name = "tasks/position_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Confirmation page and logic for deleting a position."""

    model = Position
    context_object_name = "position"
    success_url = reverse_lazy("position-list")
    template_name = "tasks/position_confirm_delete.html"


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Allows users to edit their own comments on tasks."""

    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("task-list")
    template_name = "tasks/comment_form.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return self.object.task.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Allows users to delete their own comments on tasks."""

    model = Comment
    template_name = "tasks/comment_confirm_delete.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return self.object.task.get_absolute_url()
