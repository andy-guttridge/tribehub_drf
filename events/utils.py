from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta

from notifications.models import Notification
from .serializers import UserSerializer, DurationSerializer


def make_events(event, from_date, to_date):
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

        # Find which useres have accepted the invitation and use
        # ToUserSerializer to convert to serialized user instances
        event_accepted_users = list(
            User.objects.filter(event_accepted=event).all()
        )
        accepted_user_serializer = UserSerializer(
            event_accepted_users, many=True
        )
        accepted_users = accepted_user_serializer.data

        # Use special serializer to format duration field correctly
        duration_serializer = DurationSerializer(event)
        duration = duration_serializer.data['duration']

        # Create event for each recurrence and append to list
        for recurrence in recurrences:
            event.user.profile.image.url_options.update({'secure': True})
            recurrence_event = {
                'id': event.id,
                'user': {
                    'user_id': event.user.id,
                    'display_name': event.user.profile.display_name,
                    'image': event.user.profile.image.url
                },
                'tribe': {
                    'tribe_id': event.tribe.id,
                    'tribe_name': event.tribe.name
                },
                'to': to_users,
                'start': datetime.isoformat(recurrence),
                'duration': duration,
                'recurrence_type': 'REC',
                'recurrences': None,
                'subject': event.subject,
                'category': event.category,
                'accepted': accepted_users,
            }
            recurrence_events.append(recurrence_event)

    return recurrence_events


def make_event_notifications(event, user, is_new_event=True, new_users=None):
    """
    Creates notifications for events. New events and users added to an existing
    event receive an invitation message, users already invited receive a
    message that the event has been changed.
    is_new_event = a bool indicating whether this is a newly created event
    new_users = a list of user ids that have been added to an existing event
    """
    # Iterate through users invited to this event. Check if a new event or user
    # has been newly added to the invitation, and create notification with
    # appropriate message.
    for to_user in event.to.all():
        if is_new_event or to_user in new_users:
            message = f'Invitation from {user.profile.display_name}'
        else:
            message = (
                f'{user.profile.display_name} '
                'has made a change to this event'
            )
        notification = Notification.objects.create(
            user=to_user,
            subject=event.subject,
            message=message,
            type='INV',
            event=event
        )

        if notification:
            notification.save()
