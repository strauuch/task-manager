from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, TaskType, Position, Worker


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "deadline", "status")
    list_filter = ("priority", "status", "deadline")
    search_fields = ("name", "description")
    filter_horizontal = ("assignee",)
    autocomplete_fields = ("task_type",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):

    list_display = UserAdmin.list_display + ("position",)
    list_filter = ("position",)
    search_fields = ("username", "first_name", "last_name")
    autocomplete_fields = ("position",)

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("position",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "position",
                )
            },
        ),
    )
