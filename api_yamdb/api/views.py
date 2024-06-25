from django.db.models import Avg
from django.core.exceptions import BadRequest
from rest_framework import filters, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrAdministration,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id
        )

    def get_queryset(self):
        queryset = self.get_title().reviews.all()
        return queryset

    def set_score(self):
        average_score = self.get_queryset().aggregate(Avg('score'))
        title = self.get_title()
        title.rating = average_score['score__avg']
        title.save(update_fields=["rating"])

    def perform_create(self, serializer):
        user = self.request.user
        title = self.get_title()
        if Review.objects.filter(author=user, title=title).exists():
            raise BadRequest(
                'Запрещено добавлять больше одного отзыва на одно произведение'
            )
        serializer.save(
            author=self.request.user,
            title=title,
        )
        self.set_score()

    def perform_update(self, serializer):
        serializer.save()
        self.set_score()

    def perform_destroy(self, instance):
        instance.delete()
        self.set_score()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrAdministration,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id,
        )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        title = self.get_title()
        return get_object_or_404(
            Review,
            pk=review_id,
            title=title,
        )

    def get_queryset(self):
        queryset = self.get_review().comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
            review=self.get_review(),
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = ('slug')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', 'genre__slug', 'category__slug', 'year')

    def get_queryset(self):
        queryset = Title.objects.all()
        filters = {}

        if genre_slug := self.request.query_params.get('genre', None):
            filters['genre__slug'] = genre_slug
        if category_slug := self.request.query_params.get('category', None):
            filters['category__slug'] = category_slug
        if year := self.request.query_params.get('year', None):
            filters['year'] = year
        if name := self.request.query_params.get('name', None):
            filters['name'] = name

        return queryset.filter(**filters)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
