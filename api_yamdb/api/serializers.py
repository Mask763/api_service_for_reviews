from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import EMAIL_FROM
from reviews.constants import (
    MAX_CHARFIELD_LENGTH, MAX_EMAIL_LENGTH, USER_ROLES
)
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_forbidden_username


User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор самостоятельной регистрации пользователя."""

    username = serializers.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        validators=[User.username_validator, validate_forbidden_username]
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username != user_by_email:
            if user_by_username:
                raise serializers.ValidationError(
                    {"username": "Пользователь с таким именем уже существует."}
                )
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует."}
            )

        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=EMAIL_FROM,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class UserConfirmationSerializer(serializers.Serializer):
    """Сериализатор подтверждения регистрации пользователя."""

    username = serializers.CharField(max_length=MAX_CHARFIELD_LENGTH)
    confirmation_code = serializers.CharField(max_length=MAX_CHARFIELD_LENGTH)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Некорректный код подтверждения'}
            )

        return data


class UserForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для администратора."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
            'role': {'required': False,
                     'choices': USER_ROLES},
        }


class UserSerializer(UserForAdminSerializer):
    """Сериализатор пользователя."""

    class Meta(UserForAdminSerializer.Meta):
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        request = self.context['request']
        title_id = request.parser_context.get('kwargs').get('title_id')

        if (
            request.method == "POST"
            and Review.objects.filter(
                author=request.user,
                title=title_id
            ).exists()
        ):
            raise serializers.ValidationError(
                'Запрещено добавлять больше одного отзыва на одно произведение'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('title', 'review')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление и изменение произведения."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'genre',
            'category',
            'year',
            'description',
        )

    def to_representation(self, instance):
        super().to_representation(instance)
        title_list_serializer = TitleListSerializer(instance)
        return title_list_serializer.data


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор на получение произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = Title
        fields = (
            'name', 'genre', 'category', 'year',
            'description', 'id', 'rating'
        )
