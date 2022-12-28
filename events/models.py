from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from tribes.models import Tribe
from .event_values import EventCategories, EventRepeatVals


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
        choices=EventRepeatVals.choices,
        default='NON',
        max_length=3
    )
    subject = models.CharField(max_length=25)
    category = models.CharField(
        choices=EventCategories.choices,
        default='NON',
        max_length=3)
    # accepted = ArrayField(base_field=models.IntegerField)
