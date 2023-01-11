from rest_framework import serializers
from django.utils.dateformat import format
from django.conf import settings

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications
    """
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
