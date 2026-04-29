from django.db import models
from django.conf import settings


class Report(models.Model):
    class Status(models.TextChoices):
        REPORTED = 'REPORTED', 'Reported'
        VERIFIED = 'VERIFIED', 'Verified'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REPORTED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
