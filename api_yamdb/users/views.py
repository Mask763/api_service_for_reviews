from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserForAdminSerializer,
    UserRegistrationSerializer,
    UserConfirmationSerializer,
    UserSerializer
)
from .permissions import IsAdminOnly


User = get_user_model()


class SignUp(APIView):
    """
    Представление для регистрации пользователя
    и получения кода подтверждения.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email='yamdb@localhost',
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
    """Представление для получения токена."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Некорректный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    """
    Представление для самостоятельного получения
    и редактирования данных пользователя.
    """

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserForAdminViewSet(viewsets.ModelViewSet):
    """
    Представление для получения и редактирования
    данных пользователя администратором.
    """

    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, IsAdminOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response({'detail': 'PUT метод не поддерживается.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
