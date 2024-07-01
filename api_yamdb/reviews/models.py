from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from .constants import (
    MAX_LENGTH_MAIN,
    MAX_LENGTH_SLUG,
    MAX_SCORE,
    MIN_SCORE,
)
from .validators import validate_year


User = get_user_model()


class NameSlug(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_MAIN)
    slug = models.SlugField('Слаг', unique=True, max_length=MAX_LENGTH_SLUG)

    class Meta:
        abstract = True
        ordering = ('-slug',)

    def __str__(self) -> str:
        return self.slug


class Category(NameSlug):
    """Модель Категории."""

    class Meta(NameSlug.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlug):
    """Модель Жанра."""

    class Meta(NameSlug.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        'Название проекта',
        null=False,
        max_length=MAX_LENGTH_MAIN
    )
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
    year = models.SmallIntegerField(
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True,
        max_length=MAX_LENGTH_MAIN
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'comment by {self.author} on review {self.review}'
