from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta

from notifications.models import Notification
from .serializers import UserSerializer


def make_events(request, event, from_date, to_date):
    """
    Programatically creates a list of events from the recurrences of an event
    in the database, within the range of from_date to to_date. Defaults to
    events from today and to 2 months from the from_date if from_date or
    to_date values missing.
    """
    # Default values for from_date and to_date if not specified
    from_date = datetime.now().isoformat() if from_date is None else from_date
    to_date = (
        (datetime.fromisoformat(from_date)
            + relativedelta(months=2)).isoformat()
        if to_date is None else to_date
    )

    recurrence_events = []

    # If the event has recurrences, iterate through these for the specified
    # range, and create events.
    if event.recurrences:
        recurrences = event.recurrences.between(
                    datetime.fromisoformat(from_date),
                    datetime.fromisoformat(to_date),
                    inc=True
                )

        # Find which users are invited to this event and use ToUserSerializer
        # to convert to serialized user instances.
        event_to_users = list(User.objects.filter(event=event).all())
        to_user_serializer = UserSerializer(event_to_users, many=True)
        to_users = to_user_serializer.data

        # Create event for each recurrence and append to list
        for recurrence in recurrences:
            recurrence_event = {
                'id': event.id,
                'user': {
                    'user_id': event.user.id,
                    'display_name': event.user.profile.display_name
                },
                'tribe': {
                    'tribe_id': event.tribe.id,
                    'tribe_name': event.tribe.name
                },
                'to': to_users,
                'start': datetime.isoformat(recurrence),
                'duration': event.duration,
                'recurrence_type': 'REC',
                'recurrences': None,
                'subject': event.subject,
                'category': event.category
            }
            recurrence_events.append(recurrence_event)

    return recurrence_events


def make_event_notifications(event):
    for to_user in event.to.all():
        notification = Notification.objects.create(
            to_user=to_user,
            subject=event.subject,
            message=f'Invitation from {event.user.profile.display_name}',
            type='INV',
            event=event
        )
        notification.save()
