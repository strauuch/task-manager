from django.urls import path

from tasks.views import index, TaskTypeListView, TaskListView, WorkerListView, PositionListView

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="tasks-list",
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
]
