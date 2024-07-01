import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
