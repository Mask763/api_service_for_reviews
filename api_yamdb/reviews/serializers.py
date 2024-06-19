from rest_framework import serializers

from settings.models import Title
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate_title(self, title):
        user = self.context['request'].user
        if Review.objects.filter(user=user, title=title).exists():
            raise serializers.ValidationError(
                'Запрещено добавлять больше одного отзыва на одно произведение'
            )
        return title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('title', 'review')
