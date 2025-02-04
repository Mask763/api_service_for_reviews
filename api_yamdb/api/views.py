from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (
    IsAdminOnly,
    IsAdminOrReadOnly,
    IsAuthorOrAdministration,
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleListSerializer,
    UserConfirmationSerializer,
    UserForAdminSerializer,
    UserRegistrationSerializer,
    UserSerializer
)
from reviews.mixins import CategoryGenreMixin
from .viewsets import ListCreateDestroyViewSet


User = get_user_model()


class SignUp(APIView):
    """
    Представление для регистрации пользователя
    и получения кода подтверждения.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    """Представление для получения токена."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)},
            status=status.HTTP_200_OK
        )


class UserForAdminViewSet(viewsets.ModelViewSet):
    """
    Представление для получения и редактирования
    данных пользователя администратором.
    """

    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        methods=['get', 'patch']
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title._meta.ordering)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', 'genre__slug', 'category__slug', 'year')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer
