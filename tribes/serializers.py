from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tribe
from profiles.models import Profile


class TribeSerializer(serializers.ModelSerializer):
    """
    Returns serialized representation of the given Tribe
    object and the user_id and display_name of each of the users
    who are part of the tribe.
    """
    name = serializers.ReadOnlyField()
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        """
        Retrieves all profile objects associated with the tribe,
        and returns a list of dictionaries containing user_id and
        display_name key/value pairs for each user.
        """
        queryset = Profile.objects.filter(
            tribe=obj
        ).all().order_by('display_name')
        users = []
        for profile in queryset:
            # Fix for cloudinary not serving images securely is from
            # https://stackoverflow.com/questions/48508750/how-to-force-https-in-a-django-project-using-cloudinary
            profile.image.url_options.update({'secure': True})
            user_dict = {
                'user_id': profile.user.id,
                'display_name': profile.display_name,
                'profile_image': profile.image.url,
            }
            users.append(user_dict)
        return users

    class Meta:
        model = Tribe
        fields = ['name', 'users']
