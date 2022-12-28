from django.db import models
from django.contrib.auth.models import User

from events.models import Event
import notification_values


class Notification(models.Model):
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification'
    )
    date = models.DateTimeField,
    subject = models.CharField(max_length=25)
    message = models.CharField(max_length=200)
    type = models.CharField(
        choices=notification_values.NotificationTypes,
        default='NON',
        max_length=3
    )
    event = models.ForeignKey(Event, default=None)
