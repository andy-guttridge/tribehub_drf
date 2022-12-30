from rest_framework import generics, permissions
from .models import Tribe
from .serializers import TribeSerializer


class TribeList(generics.ListAPIView):
    """
    Provides details of the current authenticated user's tribe.
    Returns the name of the tribe and a list of key/value pairs
    with the user_id and display_name of each user who is part of the tribe.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TribeSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Tribe.objects.filter(pk=user.profile.tribe.pk)
        return queryset
