from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUp, TokenObtainView, UserForAdminViewSet

v1_router = DefaultRouter()
v1_router.register('users', UserForAdminViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainView.as_view(),
        name='token_obtain'
    ),
    path('v1/', include(v1_router.urls)),
]
