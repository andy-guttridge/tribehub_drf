from rest_framework import serializers
from django.utils.dateformat import format
from django.conf import settings

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications
    """
    date_created = serializers.DateTimeField(format='iso-8601', default_timezone=None)

    class Meta:
        model = Notification
        fields = [
            'id',
            'to_user',
            'date_created',
            'subject',
            'message',
            'type',
            'event'
        ]
