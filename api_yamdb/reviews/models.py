from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# from api.models import User, Title
from settings.models import Title


class Review(models.Model):
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='reviews')
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'review by {self.author} on title {self.title}'


class Comment(models.Model):
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return f'comment by {self.author} on review {self.review}'
