from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        },
        validators=[AbstractUser.username_validator],
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.'
        },
        verbose_name='Email',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=10,
        choices=(
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Administrator'),
        ),
        default='user',
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            ),
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Сокращённая категория', unique=True, max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField('Жанр',max_length=256)
    slug = models.SlugField('Жанр сокращённо', unique=True, max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField('Название проекта', null=False, max_length=256)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='genres'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    year = models.IntegerField(default=1850)
    description = models.TextField('Описание', blank=True, max_length=256)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name
