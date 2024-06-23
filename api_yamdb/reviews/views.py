from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import BadRequest

from api_yamdb.models import (
    Title,
)
from reviews.models import (
    Review,
    Comment,
)
from reviews.serializers import (
    ReviewSerializer,
    CommentSerializer,
)
from reviews.permissions import IsAuthorOrModeratorOrAdmin


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return (IsAuthorOrModeratorOrAdmin(),)
        return super().get_permissions()

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
        if Review.objects.filter(author=user, title=self.get_title()).exists():
            raise BadRequest(
            'Запрещено добавлять больше одного отзыва на одно произведение'
        )
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )
        self.set_score()


    def perform_update(self, serializer):
        serializer.save()
        self.set_score()
    
    def perform_destroy(self, instance):
        instance.delete()
        self.set_score()


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return (IsAuthorOrModeratorOrAdmin(),)
        return super().get_permissions()

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(
            Title,
            pk=title_id,
        )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review,
            pk=review_id,
            title=self.get_title(),
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
