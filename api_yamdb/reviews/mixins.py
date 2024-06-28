from django.db import models
from rest_framework import filters

from .constants import MAX_LENGTH_MAIN
from users.permissions import IsAdminOrReadOnly


class NameSlugMixin(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_MAIN)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.slug


class CategoryGenreMixin:
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
