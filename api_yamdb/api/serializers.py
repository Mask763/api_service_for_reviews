from rest_framework import serializers

from reviews.models import Category, Title, Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""
    class Meta:
        model = Category
        fields = ('name', 'slug', 'id')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализвтор жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug', 'id')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление и изменение произведения."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year', 'description', 'id')


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор на получение произведения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = (
            'name', 'genre', 'category', 'year',
            'description', 'id', 'rating'
        )
