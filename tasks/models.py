import uuid
from django.db import models
from django.conf import settings


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        db_index=True,
    )
    title = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    last_deferred = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title[:30]

    def get_user_tasks(self):
        return self.objects.filter(user=self.user).order_by("last_deferred")

    def count_user_tasks(self):
        return self.get_user_tasks.count()

    def get_user_completed_tasks(self):
        return self.get_user_tasks.filter(is_completed=True)

    def get_user_incompleted_tasks(self):
        return self.get_user_tasks.filter(is_completed=False)
