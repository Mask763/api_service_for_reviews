from rest_framework import filters

from api.permissions import IsAdminOrReadOnly


class CategoryGenreMixin:
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
