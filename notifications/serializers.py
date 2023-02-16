from rest_framework import serializers

from .models import Notification
from events.serializers import EventSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications
    """
    event = EventSerializer()

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'date_created',
            'subject',
            'message',
            'type',
            'event'
        ]
