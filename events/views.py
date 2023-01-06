from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, serializers
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseBadRequest
from django_filters.rest_framework import DjangoFilterBackend
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
from .serializers import (
    EventSerializer,
    NewOrUpdateEventSerializer,
    EventResponseSerializer
)
from .filters import EventFilter
from .utils import make_events


class EventList(generics.ListCreateAPIView):
    """
    List all events for the authenticated user's tribe and create new event
    for the tribe. Optionally filter by date range specified by from_date and
    to_date URL arguments, filter by user using user argument, filter by
    category using category argument and search using search argument.
    """
    permission_classes = [IsInTribe, IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_class = EventFilter
    filterset_fields = ['start']
    search_fields = ['subject']

    def get_queryset(self):
        """
        Override get_queryset method to limit events to those attached
        to the user's own tribe.
        """
        user = self.request.user
        try:
            events_queryset = Event.objects.filter(tribe=user.profile.tribe.pk)
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_404_NOT_FOUND
            )
        return events_queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer depending on HTTP method.
        """
        # Technique to override method to select appropriate serializer from
        # https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
        if self.request.method == 'POST':
            return NewOrUpdateEventSerializer
        else:
            return EventSerializer

    def list(self, request, *args, **kwargs):
        """
        Override list method to programatically create events based on any
        recurrences and append to response data.
        """
        response = super().list(request, args, kwargs)
        user = request.user

        # Get unfiltered events in order to find any events before the
        # specified time range filter that might have recurrences.
        events = Event.objects.filter(tribe=user.profile.tribe.pk)

        # Apply search, category and user filters to unfiltered_events,
        # as we need to filter events that fall outside of the specified
        # time range that might have recurrences.
        subject_search = request.query_params.get('search')
        # How to search on many to many fields from
        # https://stackoverflow.com/questions/4507893/django-filter-many-to-many-with-contains
        if subject_search is not None:
            events = events.filter(subject__icontains=subject_search)
        to = request.query_params.get('to')
        if to is not None and to.isdigit():
            events = events.filter(to__in=[to])
        category_filter = request.query_params.get('category')
        if category_filter is not None:
            events = events.filter(category=category_filter)

        # Get from_date and to_date kwargs from URL arguments so these
        # can be used to limit any recurrences.
        # How to access URL parameters as kwargs from
        # https://stackoverflow.com/questions/51042871/how-to-access-url-kwargs-in-generic-api-views-listcreateapiview-to-be-more-spec
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        # Find recurrences within specified date range for all events and
        # append to response data.
        for event in events:
            recurrence_events = make_events(request, event, from_date, to_date)
            response.data['results'].extend(recurrence_events)
            response.data['count'] = (
                response.data['count'] + len(recurrence_events)
            )
        return response

    def perform_create(self, serializer):
        """
        Override create method to add user and tribe to new Event object.
        Also check if users invited to the event are part of the same tribe,
        and raise validation error if not.
        """
        for to_user_str in self.request.data.get('to'):
            try:
                to_user = User.objects.filter(id=int(to_user_str)).first()
            except TypeError as e:
                raise HttpResponseBadRequest
            if to_user.profile.tribe != self.request.user.profile.tribe:
                print(to_user.profile.tribe, self.request.user.profile.tribe)
                raise serializers.ValidationError(
                    {
                        'to': 'Users who are not part of this tribe cannot '
                        'be invited.'
                    }
                )
        serializer.save(
            user=self.request.user,
            tribe=self.request.user.profile.tribe
        )


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Event detail view providing GET, PUT and DELETE functionality
    for events.
    """
    permission_classes = [
        IsThisTribeAdminOrOwner | IsInTribeReadOnly,
        IsAuthenticated
    ]

    def get_queryset(self):
        """
        Override get_queryset method to limit events to those attached
        to the user's own tribe.
        """
        user = self.request.user
        try:
            events_queryset = Event.objects.filter(tribe=user.profile.tribe.pk)
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_404_NOT_FOUND
            )
        return events_queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer depending on HTTP method.
        """
        # Technique to override method to select appropriate serializer from
        # https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
        if self.request.method == 'GET':
            return EventSerializer
        else:
            return NewOrUpdateEventSerializer

    def perform_update(self, serializer):
        """
        Check if users invited to the event are part of the same tribe,
        and raise validation error if not.
        """
        for to_user_str in self.request.data.get('to'):
            try:
                to_user = User.objects.filter(id=int(to_user_str)).first()
            except TypeError as e:
                raise HttpResponseBadRequest
            if to_user.profile.tribe != self.request.user.profile.tribe:
                print(to_user.profile.tribe, self.request.user.profile.tribe)
                raise serializers.ValidationError(
                    {
                        'to': 'Users who are not part of this tribe cannot '
                        'be invited.'
                    }
                )
            serializer.save()


class EventResponse(APIView):
    """
    Handle user response to event invitation. Accepts data in the form:
    {"event_response":"accept" or "decline"}
    """
    permission_classes = [IsAuthenticated, IsInTribe]

    def post(self, request, pk):
        """
        Post method to handle user posting accept or decline response.
        """
        serializer = EventResponseSerializer(data=request.data)
        if serializer.is_valid():
            # Get user response from serializer and user making the request
            user_response = serializer.validated_data.get('event_response')
            user = request.user

            # Retrieve the appropriate event from the DB
            try:
                event = Event.objects.filter(id=pk).first()
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Check user is authenticated and a member of the relevant tribe,
            # then check if user is invited to the event
            self.check_object_permissions(request, event)
            if not event.to.filter(pk=user.pk).exists():
                return Response(
                    'Users who are not invited to this event cannot respond.',
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Handle accept or decline in the DB and return appropriate
            # responses
            if user_response == 'accept':
                try:
                    event.accepted.add(user)
                    return Response(
                        {'success': 'The invitation has been accepted.'},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        str(e),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                try:
                    event.accepted.remove(user)
                    return Response(
                        {'success': 'The invitation has been declined.'},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        str(e),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        # If we got to here, we must have received a bad request.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
