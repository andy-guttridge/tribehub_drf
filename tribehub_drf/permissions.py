from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from profiles.models import Profile


class IsTribeAdmin(BasePermission):
    """
    Custom permission to determine if user has family admin status.
    """
    def has_permission(self, request, view):
        profile = Profile.objects.filter(user=request.user).first()
        return profile.is_admin
