from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for contacts
    """
    tribe = serializers.SerializerMethodField()

    def get_tribe(self, obj):
        """
        Create serialized representation of tribe including
        id and tribe name.
        """
        return (
            {
                'tribe_id': obj.tribe.id,
                'tribe_name': obj.tribe.name
            }
        )

    class Meta:
        model = Contact
        fields = [
            'id',
            'tribe',
            'category',
            'title',
            'first_name',
            'last_name',
            'phone',
            'email'
        ]
