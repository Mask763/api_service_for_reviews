from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import (
    ReviewsViewSet,
    CommentsViewSet,
)

router = DefaultRouter()
router.register('comments', CommentsViewSet, basename='comments')
router.register('', ReviewsViewSet, basename='reviews')
urlpatterns = [
    path('', include(router.urls)),
]
# urlpatterns = [
#   path(r'titles/(?P<title_id>\d+)/reviews/', include('review.urls')),
# ]
