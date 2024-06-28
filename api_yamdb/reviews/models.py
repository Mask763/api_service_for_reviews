from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from .constants import MAX_LENGTH_MAIN
from .mixins import NameSlugMixin
from .service import validate_year


User = get_user_model()


class Category(NameSlugMixin):
    """Модель Категории."""

    class Meta:
        ordering = ('-slug',)


class Genre(NameSlugMixin):
    """Модель Жанра."""

    class Meta:
        ordering = ('-slug',)


class Title(models.Model):
    """Модель Фильма."""
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
