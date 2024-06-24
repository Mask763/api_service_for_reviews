from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentsViewSet,
    GenreViewSet,
    ReviewsViewSet,
    TitleViewSet
)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register(
    r'(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
v1_router.register('', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
