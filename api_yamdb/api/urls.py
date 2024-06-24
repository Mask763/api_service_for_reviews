from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryViewSet,
    TitleViewSet,
    GenreViewSet
)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/titles/<int:title_id>/reviews/', include('reviews.urls')),
]
