from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.http import Http404
from django_filters import rest_framework as filters
from datetime import datetime
import dateutil.parser
from tribehub_drf.permissions import (
    IsTribeAdmin,
    IsThisTribeAdmin,
    IsThisTribeAdminOrOwner,
    IsInTribeReadOnly,
    IsInTribe
)
from tribes.models import Tribe
from profiles.models import Profile
from .models import Event
from .serializers import EventSerializer, ToUserSerializer
from .filters import EventFilter
from .utils import make_events


class EventList(generics.ListCreateAPIView):
    """
    List all events for the authenticated user's tribe and create new event
    for the tribe. Optionally filter by date range specified by from_date and
    to_date URL arguments.
    """
    serializer_class = EventSerializer
    permission_classes = [IsInTribe]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    filterset_fields = ['start']

    def get_queryset(self):
        """
        Override get_queryset method to limit events to those attached
        to the user's own tribe.
        """
        user = self.request.user
        events_queryset = Event.objects.filter(tribe=user.profile.tribe.pk)
        return events_queryset

    def list(self, request, *args, **kwargs):
        """
        Override list method to programatically create events based on any
        recurrences and append to response data.
        """
        response = super().list(request, args, kwargs)
        user = request.user

        # Get unfiltered events in order to find any events before the
        # specified time range filter that might have recurrences.
        unfiltered_events = Event.objects.filter(tribe=user.profile.tribe.pk)

        # Get from_date and to_date kwargs from URL arguments so these
        # can be used to limit any recurrences.
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        # Find recurrences within specified date range for all events and
        # append to response data.
        for event in unfiltered_events:
            recurrence_events = make_events(request, event, from_date, to_date)
            response.data['results'].extend(recurrence_events)
            response.data['count'] = (
                response.data['count'] + len(recurrence_events)
            )
        return response
