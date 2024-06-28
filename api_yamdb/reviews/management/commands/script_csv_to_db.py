import os
import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model

from ...models import Category, Genre, Title, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Imports data from CSV files into the database'

    def handle(self, *args, **kwargs):
        csv_dir = os.path.join(settings.BASE_DIR, 'static', 'data')

        # Импорт данных из category.csv
        with open(os.path.join(csv_dir, 'category.csv'), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

        # Импорт данных из genre.csv
        with open(os.path.join(csv_dir, 'genre.csv'), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

        with open(csv_dir + '/titles.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title, created = Title.objects.get_or_create(
                    name=row['name'],
                    year=int(row['year'])
                )
                if row['category']:
                    categories = Category.objects.filter(name__in=row['category'].split(','))
                    title.category = categories.first() if categories.exists() else None
                title.genre.set(Genre.objects.filter(name__in=row['genre'].split(',')))  # Исправлено здесь

        # Импорт данных из review.csv
        with open(os.path.join(csv_dir, 'review.csv'), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review_id = int(row['review_id'])
                text = row['text']
                author_id = int(row['author'])
                pub_date = parse_datetime(row['pub_date'])

                author = User.objects.get(id=author_id)
                Review.objects.create(
                    review_id=review_id,
                    text=text,
                    author=author,
                    pub_date=pub_date
                )

        # Импорт данных из comments.csv
        with open(os.path.join(csv_dir, 'comments.csv'), mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                author_id = int(row['author'])
                review_id = int(row['review_id'])
                title_id = int(row['title'])
                text = row['text']
                pub_date = parse_datetime(row['pub_date'])

                author = User.objects.get(id=author_id)
                review = Review.objects.get(review_id=review_id)
                title = Title.objects.get(id=title_id)

                Comment.objects.create(
                    author=author,
                    review=review,
                    title=title,
                    text=text,
                    pub_date=pub_date
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))