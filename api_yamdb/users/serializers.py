from django.contrib.auth import get_user_model
from rest_framework import serializers

from .config import WRONG_USERNAMES


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор самостоятельной регистрации пользователя."""

    username = serializers.CharField(
        max_length=150,
        validators=[User.username_validator]
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"username": "Пользователь с таким именем уже существует."}
                )

        if User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {"email": "Пользователь с таким email уже существует."}
                )

        return data

    def validate_username(self, value):
        """Проверка на запрещенные имена пользователей."""
        if value in WRONG_USERNAMES:
            raise serializers.ValidationError(
                'Имя пользователя "me" недопустимо.'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class UserConfirmationSerializer(serializers.Serializer):
    """Сериализатор подтверждения регистрации пользователя."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    username = serializers.CharField(
        max_length=150,
        validators=[User.username_validator],
    )
    email = serializers.EmailField(
        max_length=254,
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    bio = serializers.CharField()
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"username": "Пользователь с таким именем уже существует."}
                )

        if User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {"email": "Пользователь с таким email уже существует."}
                )

        return data

    def validate_username(self, value):
        """Проверка на запрещенные имена пользователей."""
        if value in WRONG_USERNAMES:
            raise serializers.ValidationError(
                'Имя пользователя "me" недопустимо.'
            )
        return value

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


class UserForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для администратора."""

    username = serializers.CharField(
        max_length=150,
        validators=[User.username_validator],
    )
    email = serializers.EmailField(
        max_length=254,
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(
        required=False,
        choices=(
            ('user', 'User'),
            ('admin', 'Admin'),
            ('moderator', 'Moderator')
        ),
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"username": "Пользователь с таким именем уже существует."}
                )

        if User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {"email": "Пользователь с таким email уже существует."}
                )

        return data

    def validate_username(self, value):
        """Проверка на запрещенные имена пользователей."""
        if value in WRONG_USERNAMES:
            raise serializers.ValidationError(
                'Имя пользователя "me" недопустимо.'
            )
        return value

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
