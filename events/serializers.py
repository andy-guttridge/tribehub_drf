from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Event


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to turn user data into the correct format for
    deserialization of events, and when JSON event data is created
    programatically to represent repeat events for list view.
    """
    user_id = serializers.ReadOnlyField(source='id')
    display_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        return obj.profile.display_name

    def get_image(self, obj):
        return obj.profile.image.url

    class Meta:
        model = User
        fields = [
            'user_id',
            'display_name',
            'image',
        ]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for deserializing existing events.
    """
    id = serializers.ReadOnlyField()
    user = serializers.SerializerMethodField()
    tribe = serializers.SerializerMethodField()
    to = UserSerializer(many=True)
    accepted = UserSerializer(many=True)

    def get_user(self, obj):
        return (
            {
                'user_id': obj.user.id,
                'display_name': obj.user.profile.display_name,
                'image': obj.user.profile.image.url,
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


class NewOrUpdateEventSerializer(serializers.ModelSerializer):
    """
    Serializer used for create and update of events.
    """
    class Meta:
        model = Event
        fields = [
            'to',
            'start',
            'duration',
            'recurrence_type',
            'subject',
            'category',
        ]


class EventResponseSerializer(serializers.BaseSerializer):
    """
    Serialize and validate incoming user responses to event invitations.
    """
    def to_internal_value(self, data):
        event_response = data.get('event_response')
        if not event_response:
            raise serializers.ValidationError(
                {'event_response': 'An event response is required.'}
            )
        if (
            (event_response != 'accept') and
            (event_response != 'decline')
        ):
            raise serializers.ValidationError(
                {'event_response': 'Value must equal accept or decline.'}
            )
        return {
            'event_response': event_response
        }
