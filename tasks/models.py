import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


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
    last_deferred = models.DateTimeField(default=timezone.now())
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title[:30]
