from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from rest_framework.permissions import AllowAny, IsAuthenticated

from settings.models import (
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
from reviews.permissions import IsAuthor, IsModerator, IsAdmin


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = IsAuthor, IsModerator, IsAdmin
    pagination_class = LimitOffsetPagination

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         self.permission_classes = (AllowAny,)
    #     if self.action in ('create',):
    #         self.permission_classes = (IsAuthenticated,)
    #     if self.action in ('update', 'destroy'):
    #             self.permission_classes = (IsAuthor, IsModerator, IsAdmin,)
    #     return super().get_permissions()

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
        average_score = get_queryset(self).aggregate(Avg('score'))
        get_title(self).update(score=round(average_score))

    def perform_create(self, serializer):
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
    # permission_classes = (IsAuthor, IsModerator, IsAdmin,)
    pagination_class = LimitOffsetPagination

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         self.permission_classes = (AllowAny,)
    #     if self.action in ('create',):
    #         self.permission_classes = (IsAuthenticated,)
    #     if self.action in ('update', 'destroy'):
    #             self.permission_classes = (IsAuthor, IsModerator, IsAdmin,)
    #     return super().get_permissions()

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
