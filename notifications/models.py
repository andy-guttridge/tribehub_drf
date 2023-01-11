from django.db import models
from django.contrib.auth.models import User

from events.models import Event
from .notification_values import NotificationTypes


class Notification(models.Model):
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification'
    )
    date_created = models.DateTimeField(
        models.DateTimeField(auto_now=True)
    ),
    subject = models.CharField(max_length=25)
    message = models.CharField(max_length=200)
    type = models.CharField(
        choices=NotificationTypes.choices,
        default='NON',
        max_length=3
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        default=None)
