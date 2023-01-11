from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tribehub_drf.permissions import IsOwner
from .serializers import NotificationSerializer
from .models import Notification


class NotificationsList(generics.ListAPIView):
    """
    List all notifications for the current user
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Override get_queryset method to limit notifications only to
        the current user's
        """
        user = self.request.user
        notifications_queryset = Notification.objects.filter(user=user)
        return notifications_queryset


class NotificationDestroy(generics.DestroyAPIView):
    """
    Delete the specified notification. Only the owner
    of the notification can perform this action.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Override get_queryset method to limit notifications only to
        the current user's
        """
        user = self.request.user
        notifications_queryset = Notification.objects.filter(user=user)
        return notifications_queryset
