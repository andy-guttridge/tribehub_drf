from rest_framework import serializers
from django.contrib.auth.models import User

from profiles.models import Profile
from .models import Event


class ToUserSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='id')
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        return obj.profile.display_name

    class Meta:
        model = User
        fields = [
            'user_id',
            'display_name'
        ]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for events
    """
    id = serializers.ReadOnlyField()
    user = serializers.SerializerMethodField()
    tribe = serializers.SerializerMethodField()
    to = ToUserSerializer(many=True)

    def get_user(self, obj):
        return (
            {
                'user_id': obj.user.id,
                'display_name': obj.user.profile.display_name
            }
        )

    def get_tribe(self, obj):
        return (
            {
                'tribe_id': obj.tribe.id,
                'tribe_name': obj.tribe.name
            }
        )

    class Meta:
        model = Event
        fields = [
            'id',
            'user',
            'tribe',
            'to',
            'start',
            'duration',
            'recurrence_type',
            'subject',
            'category',
            'accepted',
        ]
