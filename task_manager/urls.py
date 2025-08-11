import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from task_manager import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("tasks.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
