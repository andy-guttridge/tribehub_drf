from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from tribes.models import Tribe
import event_values


class Event(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user'
    )
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    to = models.ManyToManyField(User, related_name='event')
    start = models.DateTimeField
    duration = models.DurationField
    repeat = models.CharField(
        choices=event_values.EventRepeatVals.choices,
        max_length=3
    )
    subject = models.CharField(max_length=25)
    category = models.CharField(
        choices=event_values.EventCategories.choices,
        max_length=3)
    accepted = ArrayField(base_field=models.IntegerField)
