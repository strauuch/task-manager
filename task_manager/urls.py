from django.contrib import admin
from django.urls import path, include

from tasks.views import TaskTypeListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),
]
