from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task
from .forms import TaskForm


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy("tasks:select_task"))
    return render(request, "tasks/index.html")


class CreateTaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "tasks/create_task.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect("tasks:select_task")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    if not task.user == user:
        raise PermissionDenied("You can only delete your own tasks.")
    if request.method == "POST":
        task.delete()
        return redirect("tasks:my_tasks")
    return HttpResponseNotAllowed(["POST"])


@login_required
def select_task(request):
    user = request.user
    task = (
        Task.objects.filter(user=user, is_completed=False)
        .order_by("last_deferred")
        .first()
    )
    return render(request, "tasks/select_task.html", {"task": task})


@login_required
def focus(request):
    user = request.user
    focus_task = (
        Task.objects.filter(user=user, is_completed=False)
        .order_by("last_deferred")
        .first()
    )

    return render(request, "tasks/focus.html", {"focus_task": focus_task})


@login_required
def defer_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    if not task.user == user:
        raise PermissionDenied("You can only manage your own tasks.")
    if request.method == "POST":
        task.last_deferred = timezone.now()
        task.save()
        messages.success(request, "Task Deferred")

    return redirect("tasks:select_task")


@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    if not task.user == user:
        raise PermissionDenied("You can only manage your own tasks.")
    if request.method == "POST":
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        messages.success(request, "Task Completed!")

    return redirect("tasks:select_task")  # change depending on request source


@login_required
def my_tasks(request):
    user = request.user
    tasks = Task.objects.filter(user=user, is_completed=False).order_by("last_deferred")
    return render(request, "tasks/my_tasks.html", {"tasks": tasks})


@login_required
def my_stats(request):
    return render(request, "tasks/my_stats.html")
