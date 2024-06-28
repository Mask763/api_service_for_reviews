from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404


from .filters import TitleFilter
from users.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrAdministration,
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleListSerializer
)
from reviews.mixins import CategoryGenreMixin
from .viewsets import ListCreateDestroyViewSet


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrAdministration,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title,
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrAdministration,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Review,
            pk=review_id,
            title=title_id,
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            pk=title_id,
        )
        serializer.save(
            author=self.request.user,
            title=title,
            review=self.get_review(),
        )


class CategoryViewSet(CategoryGenreMixin, ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin, ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', 'genre__slug', 'category__slug', 'year')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer
