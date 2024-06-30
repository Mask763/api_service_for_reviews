from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import EMAIL_FROM
from .constants import MAX_CHARFIELD_LENGTH, MAX_EMAIL_LENGTH, USER_ROLES
from .validators import validate_forbidden_username


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
