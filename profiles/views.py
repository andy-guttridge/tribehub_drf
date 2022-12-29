from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from tribes.models import Tribe
from profiles.models import Profile
from .serializers import NewTribeSerializer


class RegisterNewTribe(APIView):
    """
    Creates new user with family admin status, an associated user profile
    and a new Tribe.
    """
    def post(self, request):
        serializer = NewTribeSerializer(data=request.data)
        # Use serializer to validate data, and if valid create new user,
        # tribe and profile objects. Try to save and either return success code
        # or errors.
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data.get('username'),
                password=serializer.validated_data.get('password')
            )
            tribe = Tribe.objects.create(
                name=serializer.validated_data.get('tribename')
            )
            profile = Profile.objects.create(
                user=user,
                display_name=serializer.validated_data.get('username'),
                tribe=tribe,
                is_admin=True,
            )
            try:
                user.save()
                tribe.save()
                profile.save()
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
