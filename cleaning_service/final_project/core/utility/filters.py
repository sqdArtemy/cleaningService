from django_filters import rest_framework as filters

from core.models import Service, User, Order, Notification


# Some base filters
class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):  # Declaring filter for Many to many fields
    pass


# Filters for user model
class UserFilter(filters.FilterSet):
    rating = filters.RangeFilter()
    role = filters.CharFilter(field_name='role__role')
    services = CharFilterInFilter(field_name='services__name', lookup_expr='in')

    class Meta:
        model = User
        fields = ('rating', 'city', 'country', 'services', 'role',)


# Filter for services
class ServiceFilter(filters.FilterSet):
    cost = filters.RangeFilter()

    class Meta:
        model = Service
        fields = ('cost',)


# Filters for order model
class OrderFilter(filters.FilterSet):
    total_cost = filters.RangeFilter()

    class Meta:
        model = Order
        fields = ('total_cost', 'request', 'accepted')


# Filters for notification model
class NotificationFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__username')

    class Meta:
        model = Notification
        fields = ('seen', 'accepted', 'user', 'request')
