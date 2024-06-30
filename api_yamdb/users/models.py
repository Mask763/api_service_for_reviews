from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    MAX_CHARFIELD_LENGTH,
    MAX_EMAIL_LENGTH,
    USER_ROLES,
    USER_ROLE_ADMIN,
    USER_ROLE_MODERATOR
)
from .validators import validate_forbidden_username


class ApplicationUser(AbstractUser):
    username = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        },
        validators=[
            AbstractUser.username_validator,
            validate_forbidden_username
        ],
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.'
        },
        verbose_name='Email',
    )
    first_name = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        verbose_name='Фамилия',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=max([len(role[0]) for role in USER_ROLES]),
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == USER_ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == USER_ROLE_MODERATOR
