from django_filters import rest_framework as filters
from .models import Event

# Approach to creating a custom filter for date ranges from
# https://stackoverflow.com/questions/37183943/django-how-to-filter-by-date-with-django-rest-framework


class EventFilter(filters.FilterSet):
    """
    Custom filter for retrieving events within a specific date range
    """
    from_date = filters.IsoDateTimeFilter(
        field_name='start',
        lookup_expr='gte'
    )
    to_date = filters.IsoDateTimeFilter(field_name='start', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['start', 'to', 'user', 'category']
