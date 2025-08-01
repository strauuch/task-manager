from django.urls import path

from tasks.views import index, TaskTypeListView, TaskListView, WorkerListView

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
        "workers/",
        WorkerListView.as_view(),
        name="workers-list",
    ),
]
