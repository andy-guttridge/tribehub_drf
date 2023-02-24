from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, serializers
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django_filters.rest_framework import DjangoFilterBackend
from django.db import DatabaseError
from django.db.models import Q
from tribehub_drf.permissions import (
    IsThisTribeAdminOrOwner,
    IsInTribeReadOnly,
    IsInTribe
)
from .models import Event
from .serializers import (
    EventSerializer,
    NewOrUpdateEventSerializer,
    EventResponseSerializer
)
from .filters import EventFilter
from .utils import make_events, make_event_notifications


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
    search_fields = ['subject']

    def get_queryset(self):
        """
        Override get_queryset method to limit events to those attached
        to the user's own tribe.
        """
        user = self.request.user
        try:
            events_queryset = Event.objects.filter(
                tribe=user.profile.tribe.pk).order_by('start')
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
        userVal = request.query_params.get('user')
        if userVal is not None and userVal.isdigit():
            events = events.filter(user=userVal)
        category_filter = request.query_params.get('category')
        if category_filter is not None:
            events = events.filter(category=category_filter).all()
        events = events.order_by('start')

        # Get from_date and to_date kwargs from URL arguments so these
        # can be used to limit any recurrences.
        # How to access URL parameters as kwargs from
        # https://stackoverflow.com/questions/51042871/how-to-access-url-kwargs-in-generic-api-views-listcreateapiview-to-be-more-spec
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        # Find recurrences within specified date range for all events,
        # create JSON for these, and append to response data.
        for event in events:
            recurrence_events = make_events(event, from_date, to_date)
            response.data['results'].extend(recurrence_events)
            response.data['count'] = (
                response.data['count'] + len(recurrence_events)
            )

        # Sort events by start date before returning them
        response.data['results'] = sorted(
            response.data['results'], key=lambda d: d['start']
        )
        return response

    def perform_create(self, serializer):
        """
        Override create method to add user and tribe to new Event object.
        Also check if users invited to the event are part of the same tribe,
        and raise validation error if not.
        """
        # Retrieve users invited to the event
        to_users_list = self.request.data.getlist('to[]')
        if to_users_list != ['']:

            # Iterate through user ids received in POST request, and check each
            # one is a member of the event creator's tribe and raise validation
            # error if we find someone who is not in the tribe.
            for to_user_str in to_users_list:
                try:
                    to_user = User.objects.filter(id=int(to_user_str)).first()
                except TypeError as e:
                    raise HttpResponseBadRequest
                if to_user.profile.tribe != self.request.user.profile.tribe:
                    raise serializers.ValidationError(
                        {
                            'to': 'Users who are not part of this '
                            'tribe cannot be invited.'
                        }
                    )
        else:
            # Serializer needs an empty list if noone is invited
            to_users_list = []
        # Create the event
        event = serializer.save(
            to=to_users_list,
            user=self.request.user,
            tribe=self.request.user.profile.tribe
        )
        # Create notifications for each user invited
        try:
            make_event_notifications(event)
        except Exception as e:
            raise DatabaseError(
                'An error occurred creating an event notification'
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
        # new_users will contain ids of any users who have just been
        # invited to this existing event.
        new_users = []

        # Retrieve users invited to the event
        to_users_list = self.request.data.getlist('to[]')

        if to_users_list != ['']:
            # Check all users invited are part of the event creator's tribe
            for to_user_str in to_users_list:
                try:
                    to_user = User.objects.filter(id=int(to_user_str)).first()
                except TypeError as e:
                    raise HttpResponseBadRequest
                if to_user.profile.tribe != self.request.user.profile.tribe:
                    raise serializers.ValidationError(
                        {
                            'to': 'Users who are not part of this '
                            'tribe cannot be invited.'
                        }
                    )
                # If user was not already invited to this event,
                # add them to new_users list
                if to_user not in list(
                    User.objects.filter(event=self.get_object().id).all()
                ):
                    new_users.append(to_user)

        # Create event and create notifications for all invited users
        event = serializer.save(to=to_users_list)
        try:
            make_event_notifications(
                event,
                is_new_event=False,
                new_users=new_users
            )
        except Exception as e:
            raise DatabaseError(
                'An error occurred creating an event notification'
            )


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
            event = Event.objects.filter(id=pk).first()

            # Check user is authenticated and a member of the relevant tribe,
            # then check if user is invited to the event.
            # Make sure to catch any references to events that don't exist.

            try:
                self.check_object_permissions(request, event)
            except (PermissionDenied, NotAuthenticated) as e:
                return Response(
                    str(e),
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_404_NOT_FOUND
                )

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
                        {'detail': 'The invitation has been accepted.'},
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
                        {'detail': 'The invitation has been declined.'},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        str(e),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        # If we got to here, we must have received a bad request.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
