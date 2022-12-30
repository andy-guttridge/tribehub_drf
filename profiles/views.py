from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from django.http import Http404
from tribehub_drf.permissions import (
    IsTribeAdmin,
    IsThisTribeAdmin,
    IsThisTribeAdminOrOwner,
    IsInTribeReadOnly
)
from tribes.models import Tribe
from profiles.models import Profile
from .serializers import (
    NewTribeSerializer,
    NewUserSerializer,
    ProfileSerializer
)


class TribeAccount(APIView):
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
                {
                    'username': serializer.validated_data['username'],
                    'tribename': serializer.validated_data['tribename']
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccount(APIView):
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
                {
                    'username': serializer.validated_data['username'],
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    """
    Makes user inactive, deletes associated profile, and
    deletes the tribe if they are the tribe admin. Action can
    only be performed by user on their own account or by the tribe admin
    for other user accounts.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Retrieve users and profiles from the DB, both for
        # the user making the request and user to be deleted.
        user = request.user
        profile = Profile.objects.filter(
            user=user
        ).first()
        user_to_del = User.objects.filter(
            pk=pk
        ).first()
        profile_to_del = Profile.objects.filter(
            user=pk
        ).first()

        if user_to_del is None or profile_to_del is None:
            raise Http404

        # Make requested account inactive only if the user is requesting the
        # action on their own account or the user is the tribe admin.
        if user == user_to_del or (
            profile.is_admin and profile.tribe == profile_to_del.tribe
        ) is True:
            user_to_del.is_active = False
            try:
                user_to_del.save()
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Delete the tribe itself if this is a family admin requesting
            # deletion of their own account.
            if profile_to_del.is_admin is True and profile == profile_to_del:
                profiles_queryset = (
                    Profile.objects.filter(tribe=profile_to_del.tribe)
                )
                try:
                    for profile in profiles_queryset:
                        profile.user.is_active = False
                        profile.user.save()
                except Exception as e:
                    return Response(
                        str(e),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                profile.tribe.delete()

            # Delete requested profile and return success code.
            profile_to_del.delete()
            return Response(
                {'deleted': 'The user account has been successfully deleted.'},
                status=status.HTTP_200_OK
            )

        # If the user got this far, they don't have permission.
        return Response(
            {"detail": "You are not allowed to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Allows updating of profile by profile owner or tribe admin, and
    read only access to a specific profile to members of the same tribe.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsInTribeReadOnly | IsThisTribeAdminOrOwner]
    queryset = Profile.objects.all()

    def get_object(self):
        """
        Retrieve profile object based on user pk value, as profile and user
        pk may not be the same.
        """
        queryset = self.get_queryset()
        user_to_find = self.kwargs['pk']
        profile = queryset.filter(user=user_to_find).first()
        if profile is None:
            raise Http404
        self.check_object_permissions(self.request, profile)
        return profile
