from django.urls import path

from tasks.views import TaskTypeListView, index

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
]
