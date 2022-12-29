from rest_framework import serializers


class NewTribeSerializer(serializers.BaseSerializer):
    """
    Custome serializer class. Performs serialization and data validation,
    but doesn't save the data as the relevant view needs to create instances
    of several different models.
    """
    def to_internal_value(self, data):
        """
        Validate data and raise errors if required. If data successfully
        validated, return native Python objects.
        """
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        tribename = data.get('tribename')

        if not username:
            raise serializers.ValidationError(
                {'username': 'A username is required.'}
            )
        if len(username) > 150:
            raise serializers.ValidationError(
                {'username': 'Usernames cannot exceed 150 characters'}
            )
        if password != password2:
            raise serializers.ValidationError(
                {
                    'password': 'Both password fields must contain the same'
                    ' value.'
                }
            )
        if not tribename:
            raise serializers.ValidationError(
                {'tribename': 'A tribe name must be entered.'}
            )
        if len(tribename) > 50:
            raise serializers.ValidationError(
                {'tribename': 'Tribe names cannot exceed 50 characters.'}
            )

        return {
            'username': username,
            'password': password,
            'tribename': tribename
        }

    def to_representation(self, instance):
        """
        Serialized representation of data.
        """
        return {
            'username': instance.username,
            'password': instance.password,
            'tribename': instance.tribename,
        }
