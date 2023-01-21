from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serialize current user data. Include profile image and user id.
    """
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    display_name = serializers.ReadOnlyField(source='profile.display_name')
    is_admin = serializers.ReadOnlyField(source='profile.is_admin')
    tribe_name = serializers.ReadOnlyField(source='profile.tribe.name')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_image',
            'display_name',
            'is_admin',
            'tribe_name',
        )
