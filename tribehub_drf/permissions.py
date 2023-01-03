from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from django.contrib.auth.models import User
from profiles.models import Profile


class IsTribeAdmin(BasePermission):
    """
    Custom permission to determine if user has general tribe admin status
    (not specific to a particular tribe).
    """
    def has_permission(self, request, view):
        profile = Profile.objects.filter(user=request.user).first()
        return profile.is_admin


class IsThisTribeAdmin(BasePermission):
    """
    Custom permission to determine if user is the admin for the specific tribe
    with which the object is associated. The object being checked must have a
    tribe foreign key field.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        profile = user.profile

        return (
            profile.is_admin is True and
            obj.tribe == profile.tribe
            )


class IsThisTribeAdminOrOwner(BasePermission):
    """
    Custom permission to determine if user is the admin for the specific tribe
    with which the object is associated or the creator/owner of the object.
    The object being checked must have user and tribe foreign key fields.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Try...except block catches unauthenticated users who do not
        # have a profile object.
        try:
            profile = user.profile
        except AttributeError:
            return False

        if obj.user == profile.user:
            return True

        return (
            (profile.is_admin is True) and
            (obj.tribe == profile.tribe)
            )


class IsInTribeReadOnly(BasePermission):
    """
    Custom permission to determine if user is a member of the relevant tribe
    with which the object is associated and if the method is a SAFEMETHOD.
    If so, grant them access. Object being checked must have a tribe
    foreign key field.
    """
    def has_object_permission(self, request, view, obj):
        # Try...except block catches unauthenticated users who do not
        # have a profile object.
        try:
            profile = request.user.profile
        except AttributeError:
            return False
        if request.method in SAFE_METHODS:
            return obj.tribe == profile.tribe
        return False


class IsInTribe(BasePermission):
    """
    Custom permission to determine if user is a member of the relevant tribe
    with which the object is associated.
    If so, grant them access. Object being checked must have a tribe
    foreign key field.
    """
    def has_object_permission(self, request, view, obj):
        # Try...except block catches unauthenticated users who do not
        # have a profile object.
        try:
            profile = request.user.profile
        except AttributeError:
            return False
        return obj.tribe == profile.tribe
