from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        data = super().validate(data)
        self.validate_one_review()
        return data

    def validate_one_review(self):
        request = self.context['request']
        title_id = request.parser_context.get('kwargs').get('title_id')
        if (
            request.method == "POST"
            and Review.objects.filter(
                author=request.user,
                title=title_id
            ).exists()
        ):
            raise serializers.ValidationError(
                'Запрещено добавлять больше одного отзыва на одно произведение'
            )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('title', 'review')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre

        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление и изменение произведения."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'genre',
            'category',
            'year',
            'description',
        )

    def to_representation(self, instance):
        super().to_representation(instance)
        title_list_serializer = TitleListSerializer(instance)
        return title_list_serializer.data


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор на получение произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'name', 'genre', 'category', 'year',
            'description', 'id', 'rating'
        )

    def get_rating(self, obj):
        return obj.rating if hasattr(obj, 'rating') else None
