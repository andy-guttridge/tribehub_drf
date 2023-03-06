from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serialize current user data. Include profile image and user id.
    """
    profile_image = serializers.SerializerMethodField()
    display_name = serializers.ReadOnlyField(source='profile.display_name')
    is_admin = serializers.ReadOnlyField(source='profile.is_admin')
    tribe_name = serializers.ReadOnlyField(source='profile.tribe.name')

    def get_profile_image(self, obj):
        """
        Serializer method for profile image, to enable
        implementing a fix for cloudinary not serving images securely
        """
        # Fix for cloudinary not serving images securely is from
        # https://stackoverflow.com/questions/48508750/how-to-force-https-in-a-django-project-using-cloudinary
        obj.profile.image.url_options.update({'secure': True})
        return obj.profile.image.url

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_image',
            'display_name',
            'is_admin',
            'tribe_name',
        )
