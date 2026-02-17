from django.urls import path

from tasks.views import (
    IndexView,
    TaskTypeListView,
    TaskListView,
    WorkerListView,
    PositionListView,
    TaskDetailView,
    WorkerDetailView,
    TaskCreateView,
    TaskTypeCreateView,
    TaskTypeDetailView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskDeleteView,
    TaskUpdateView,
    WorkerCreateView,
    CommentUpdateView,
    CommentDeleteView, WorkerUpdateView, WorkerDeleteView, PositionDetailView,
)

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),

    # Task Types
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "task-types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail",
    ),
    path(
        "task-types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),

    # Tasks
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list",
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
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),

    # Positions
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list",
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail",
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),

    # Workers
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create",
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail",
    ),

    # Comments
    path(
        "comments/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
