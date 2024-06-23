from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from api_yamdb.models import Category, Genre, Title

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(
        max_length=150,
        validators=[User.username_validator],
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Пользователь с таким именем или email уже существует.'
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" недопустимо.'
            )
        return value


class UserConfirmationSerializer(serializers.Serializer):
    """Сериализатор подтверждения регистрации пользователя."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализвтор жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализватор на добавление и изменение произведения."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year', 'description', 'id')

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                'Неверно введён год!'
            )
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Название произведения не может быть длиннее 256 символов.'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор на получение произведения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='rewiews__score_avg',
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'name', 'genre', 'category', 'year',
            'description', 'id', 'rating'
        )
