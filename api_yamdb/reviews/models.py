from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
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


User = get_user_model()


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(
        'Сокращённая категория',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
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

    class Meta:
        ordering = ['name']


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        ]

    def __str__(self):
        return f'review by {self.author} on title {self.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return f'comment by {self.author} on review {self.review}'
