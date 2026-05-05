from django.db import models
from django.conf import settings


class Report(models.Model):

    class Status(models.TextChoices):
        REPORTED = 'REPORTED', 'Reported'
        VERIFIED = 'VERIFIED', 'Verified'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'

    CATEGORY_CHOICES = [
        ('Jalan Rusak', 'Jalan Rusak'),
        ('Sampah', 'Sampah'),
        ('Lampu Mati', 'Lampu Mati'),
        ('Drainase', 'Drainase'),
        ('Keamanan', 'Keamanan'),
    ]

    # user tetap ada (untuk sistem login kamu)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    location = models.CharField(max_length=255, blank=True, null=True)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REPORTED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title