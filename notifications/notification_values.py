from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypes(models.TextChoices):
    '''
    Defines NotificationTypes for use in Notification model.
    Used to determine type of notifications.
    '''
    NONE = 'NON', _('None')
    EVENT_REMINDER = 'ERM', _('Event reminder')
    INVITATION = 'INV', _('Invitation')
