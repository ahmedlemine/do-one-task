from django.urls.conf import path

from .views import (
    home,
    select_task,
    focus,
    my_tasks,
    my_stats,
    defer_task,
    mark_task_completed,
    CreateTaskView,
    delete_task,
)

app_name = "tasks"

urlpatterns = [
    path("", home, name="home"),
    path("select_task/", select_task, name="select_task"),
    path("focus/", focus, name="focus"),
    path("my_tasks/", my_tasks, name="my_tasks"),
    path("my_stats/", my_stats, name="my_stats"),
    path("defer/<uuid:task_id>/", defer_task, name="defer_task"),
    path(
        "complete/<uuid:task_id>/",
        mark_task_completed,
        name="mark_completed",
    ),
    path("delete/<uuid:task_id>/", delete_task, name="delete_task"),
    path("create/", CreateTaskView.as_view(), name="create_task"),
]
