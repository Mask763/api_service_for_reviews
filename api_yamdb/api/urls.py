from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentsViewSet,
    GenreViewSet,
    ReviewsViewSet,
    SignUp,
    TokenObtainView,
    TitleViewSet,
    UserForAdminViewSet
)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('users', UserForAdminViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainView.as_view(),
        name='token_obtain'
    ),
    path('v1/', include(v1_router.urls)),
]
