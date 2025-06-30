import django_filters
from .models import Field


class FieldFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='locations__district__region__id')
    region_name = django_filters.CharFilter(field_name='locations__district__region__name', lookup_expr='icontains')

    district = django_filters.NumberFilter(field_name='locations__district__id')
    district_name = django_filters.CharFilter(field_name='locations__district__name', lookup_expr='icontains')

    owner = django_filters.NumberFilter(field_name='owner__id')
    owner_username = django_filters.CharFilter(field_name='owner__username', lookup_expr='icontains')

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    size = django_filters.CharFilter(field_name='size', lookup_expr='icontains')
    price_per_hour = django_filters.NumberFilter(field_name='price_per_hour')
    located = django_filters.BooleanFilter(method='filter_by_location')

    class Meta:
        model = Field
        fields = [
            'region', 'region_name',
            'district', 'district_name',
            'owner', 'owner_username',
            'name', 'size', 'price_per_hour', 'located'
        ]

    def filter_by_location(self, queryset, name, value):
        if value:
            return queryset.filter(locations__isnull=False).distinct()
        else:
            return queryset.filter(locations__isnull=True).distinct()

class FieldStatusFilter(django_filters.FilterSet):
    field_id = django_filters.NumberFilter(field_name='id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    owner = django_filters.CharFilter(field_name='owner__username', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name='locations__district__region__name', lookup_expr='icontains')
    district = django_filters.CharFilter(field_name='locations__district__name', lookup_expr='icontains')
    located = django_filters.BooleanFilter(method='filter_by_location')

    class Meta:
        model = Field
        fields = ['field_id', 'name', 'owner', 'region', 'district', 'located']

    def filter_by_location(self, queryset, name, value):
        if value:
            return queryset.filter(locations__isnull=False).distinct()
        return queryset.filter(locations__isnull=True).distinct()
