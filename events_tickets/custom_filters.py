import django_filters
from events_tickets.models import Event

class EventFilter(django_filters.FilterSet):
    ticket_type = django_filters.BaseInFilter(field_name='eventtickettype__ticket_type__name')
    price = django_filters.BaseRangeFilter(field_name='eventtickettype__price')
    date = django_filters.DateFromToRangeFilter(field_name='date')
    class Meta:
        model = Event
        fields=['date','price','ticket_type']