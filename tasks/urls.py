from django.urls import path

from tasks.views import (index, TaskTypeListView, TaskListView, WorkerListView, PositionListView, TaskDetailView, WorkerDetailView, TaskCreateView, )

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-types-list",
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="tasks-list",
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="positions-list",
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="workers-list",
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail",
    ),
]
