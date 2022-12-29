from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from tribehub_drf.permissions import IsTribeAdmin
from tribes.models import Tribe
from profiles.models import Profile
from .serializers import NewTribeSerializer, NewUserSerializer


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


class RegisterNewUser(APIView):
    """
    Creates new user and an associated user profile, and associates
    their profile with that of the tribe admin who is requesting the
    account.
    """
    # Permission classes confirm only authenticated users
    # with tribe admin status can perform this action.
    permission_classes = [IsAuthenticated, IsTribeAdmin]

    def post(self, request):
        # Use serializer to validate data, and if valid create new user,
        # and profile objects. Try to save and either return success code
        # or errors. Note the user profile is automatically allocated to the
        # tribe of the authenticated user making the request.

        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                    username=serializer.validated_data.get('username'),
                    password=serializer.validated_data.get('password')
                )
            profile = Profile.objects.create(
                    user=user,
                    display_name=serializer.validated_data.get('username'),
                    tribe=Profile.objects.filter(
                            user=request.user
                        ).first().tribe,
                    is_admin=False,
                )
            try:
                user.save()
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
