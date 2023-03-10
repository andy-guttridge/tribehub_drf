from django.db import models
from django.utils.translation import gettext_lazy as _


class EventRepeatVals(models.TextChoices):
    '''
    Defines EventRepeatVals for use in Event model.
    Used to determine frequency (if any) of repeats
    of calendar events.
    '''
    NONE = 'NON', _('None')
    IS_RECURRENCE = 'REC', _('Is Recurrence')
    DAILY = 'DAI', _('Daily')
    WEEKLY = 'WEK', _('Weekly')
    TWO_WEEKLY = 'TWK', _('Two weekly')
    MONTHLY = 'MON', _('Monthly')
    YEARLY = 'YEA', _('Yearly')


class EventCategories(models.TextChoices):
    '''
    Defines EventCategories for use in Event model.
    User can choose a category for the event in the
    family calendar.
    '''
    NONE = 'NON', _('None')
    CELEBRATION = 'CEL', _('Celebration')
    CLUB = 'CLU', _('Club')
    EDUCATION = 'EDU', _('Education')
    MEDICAL = 'MED', _('Medical')
    MUSIC = 'MUS', _('Music')
    OTHER = 'OTH', _('Other')
    OUTING = 'OUT', _('Outing')
    PETS = 'PET', _('Pets')
    SHOP = 'SHO', _('Shopping')
    SPORT = 'SPO', _('Sport')
    VAC = 'VAC', _('Vacation')
    WORK = 'WOR', _('Work')
