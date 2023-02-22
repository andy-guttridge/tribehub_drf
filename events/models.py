from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
from recurrence.fields import RecurrenceField
import recurrence

from tribes.models import Tribe
from .event_values import EventCategories, EventRepeatVals


class Event(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='event_user'
    )
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    to = models.ManyToManyField(
        User,
        related_name='event',
        blank=True
    )
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
    accepted = models.ManyToManyField(User, related_name='event_accepted')

    def save(self, *args, **kwargs):
        """
        Overide Event model save method to programatically
        create RecurrenceField based on the string value of
        recurrence_type field.
        """
        # Technique for overriding save method to set fields conditionally
        # on values of other fields adapted from
        # https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields

        # Technique to use pattern matching as case statement from
        # https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement

        # Create recurrence rules based on value of recurrence_type string
        match self.recurrence_type:
            case 'DAI':
                rule = recurrence.Rule(recurrence.DAILY)
                pattern = recurrence.Recurrence(
                    dtstart=self.start + datetime.timedelta(days=1),
                    dtend=None,
                    rrules=[rule, ],
                )
            case 'WEK':
                rule = recurrence.Rule(recurrence.WEEKLY)
                pattern = recurrence.Recurrence(
                    dtstart=self.start + datetime.timedelta(weeks=1),
                    dtend=None,
                    rrules=[rule, ],
                )
            case 'TWK':
                rule = recurrence.Rule(recurrence.WEEKLY, interval=2)
                pattern = recurrence.Recurrence(
                    dtstart=self.start + datetime.timedelta(weeks=2),
                    dtend=None,
                    rrules=[rule, ],
                )
            case 'MON':
                # Create rules with fallback days for monthly recurrences with
                # dates >28, to account for differing month lengths. Code
                # adapted from
                # https://stackoverflow.com/questions/35757778/rrule-for-repeating-monthly-on-the-31st-or-closest-day
                if self.start.day == 31:
                    rule = recurrence.Rule(
                        recurrence.MONTHLY,
                        bymonthday=[28, 29, 30, 31],
                        bysetpos=-1
                    )
                elif self.start.day == 30:
                    rule = recurrence.Rule(
                        recurrence.MONTHLY,
                        bymonthday=[28, 29, 30],
                        bysetpos=-1
                    )
                elif self.start.day == 29:
                    rule = recurrence.Rule(
                        recurrence.MONTHLY,
                        bymonthday=[28, 29],
                        bysetpos=-1
                    )
                else:
                    rule = (recurrence.Rule(recurrence.MONTHLY))
                pattern = recurrence.Recurrence(
                    dtstart=self.start + relativedelta(months=1),
                    dtend=None,
                    include_dtstart=False,
                    rrules=[rule, ]
                )
            case 'YEA':
                rule = recurrence.Rule(recurrence.YEARLY)
                pattern = recurrence.Recurrence(
                    dtstart=self.start + datetime.timedelta(days=365),
                    dtend=None,
                    rrules=[rule, ],
                )
            case _:
                pattern = None

        # Save the appropriate pattern as a recurrences instance
        self.recurrences = pattern
        super(Event, self).save(*args, **kwargs)
