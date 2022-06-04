from django_filters import rest_framework as filters
from core.models import User


# Some base filters
class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):  # Declaring filter for Many to many fileds
    pass


# Filters for user model
class UserFilter(filters.FilterSet):
    rating = filters.RangeFilter()
    city = filters.CharFilter()
    role = filters.CharFilter(field_name='role__role')
    country = filters.CharFilter()
    services = CharFilterInFilter(field_name='services__name', lookup_expr='in')

    class Meta:
        model = User
        fields = ['rating', 'city', 'country', 'services', 'role']
