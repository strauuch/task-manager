import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from task_manager import settings
from tasks.views import TaskTypeListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("tasks.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
