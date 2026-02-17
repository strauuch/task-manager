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
    """View class for the task types page of the site."""

    model = TaskType
    context_object_name = "task_types"
    template_name = "tasks/task_types_list.html"
    paginate_by = 10
    search_form_class = TaskTypeSearchForm


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the task type detail page of the site."""

    model = TaskType
    context_object_name = "task_type"
    template_name = "tasks/task_types_detail.html"



class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for the create task types page of the site."""

    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task-types-list")
    template_name = "tasks/task_types_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for the update task types page of the site."""

    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("task-types-list")
    template_name = "tasks/task_types_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for the delete task types page of the site."""

    model = TaskType
    success_url = reverse_lazy("task-types-list")
    template_name = "tasks/task_types_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    """View class for the tasks page of the site."""

    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
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
    """View class for the task detail page of the site."""

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
    """View class for the task create page of the site."""

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks-list")
    template_name = "tasks/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for the task update page of the site."""

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks-list")
    template_name = "tasks/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for the task delete page of the site."""

    model = Task
    success_url = reverse_lazy("tasks-list")
    template_name = "tasks/task_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """View class for the workers page of the site."""

    model = Worker
    context_object_name = "workers"
    template_name = "tasks/workers_list.html"
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
    """View class for the worker detail page of the site."""

    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for the worker create page of the site."""

    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("workers-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for the worker update page of the site."""

    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("workers-list")
    template_name = "tasks/worker_form.html"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for the task delete page of the site."""

    model = Worker
    success_url = reverse_lazy("workers-list")
    template_name = "tasks/worker_confirm_delete.html"

class PositionListView(LoginRequiredMixin, SearchListViewMixin, generic.ListView):
    """View class for the positions page of the site."""

    model = Position
    context_object_name = "positions"
    template_name = "tasks/positions_list.html"
    paginate_by = 10
    search_form_class = PositionSearchForm

class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for the position detail page of the site."""

    model = Position
    context_object_name = "positions"
    template_name = "tasks/positions_detail.html"

class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for the create positions page of the site."""

    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("positions-list")
    template_name = "tasks/positions_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for the update positions page of the site."""

    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("positions-list")
    template_name = "tasks/positions_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for the delete positions page of the site."""

    model = Position
    success_url = reverse_lazy("positions-list")
    template_name = "tasks/positions_confirm_delete.html"


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for the update comment page of the site."""

    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("tasks-list")
    template_name = "tasks/comments_form.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return self.object.task.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for the delete comment page of the site."""

    model = Comment
    template_name = "tasks/comments_confirm_delete.html"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return self.object.task.get_absolute_url()
