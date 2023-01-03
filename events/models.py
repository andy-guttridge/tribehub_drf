from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField

from tribes.models import Tribe
from .event_values import EventCategories, EventRepeatVals


class Event(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='event_user'
    )
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    to = models.ManyToManyField(User, related_name='event')
    start = models.DateTimeField(editable=True)
    duration = models.DurationField(editable=True)
    recurrence_type = models.CharField(
        choices=EventRepeatVals.choices,
        default='NON',
        max_length=3
    )
    recurrences = RecurrenceField(null=True, blank=True)
    subject = models.CharField(max_length=25)

    category = models.CharField(
        choices=EventCategories.choices,
        default='NON',
        max_length=3)

    # How to properly define a field within an array field from
    # https://stackoverflow.com/questions/41180829/arrayfield-missing-1-required-positional-argument
    # accepted = ArrayField(
    #     base_field=models.IntegerField(null=True, blank=True),
    #     blank=True
    # )
