import csv
import os

import django
from django.conf import settings
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


User = get_user_model()

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


def load_category():
    with open(
        os.path.join(DATA_DIR, 'category.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.update_or_create(
                id=row['id'],
                defaults={'name': row['name'], 'slug': row['slug']}
            )
    print('Categories загружены')


def load_genre():
    with open(
        os.path.join(DATA_DIR, 'genre.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.update_or_create(
                id=row['id'],
                defaults={'name': row['name'], 'slug': row['slug']}
            )
    print('Genres загружены')


def load_titles():
    with open(
        os.path.join(DATA_DIR, 'titles.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'year': row['year'],
                    'category_id': row['category']
                }
            )
    print('Titles загружены')


def load_genre_title():
    with open(
        os.path.join(DATA_DIR, 'genre_title.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)
    print('Genres for titles загружены')


def load_users():
    with open(
        os.path.join(DATA_DIR, 'users.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            User.objects.update_or_create(
                id=row['id'],
                defaults={
                    'username': row['username'],
                    'email': row['email'],
                    'role': row['role'],
                    'bio': row['bio'] if row['bio'] else '',
                    'first_name': (
                        row['first_name'] if row['first_name'] else ''
                    ),
                    'last_name': row['last_name'] if row['last_name'] else ''
                }
            )
    print('Users загружены')


def load_reviews():
    with open(
        os.path.join(DATA_DIR, 'review.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.update_or_create(
                id=row['id'],
                defaults={
                    'title_id': row['title_id'],
                    'text': row['text'],
                    'author_id': row['author'],
                    'score': row['score'],
                    'pub_date': row['pub_date']
                }
            )
    print('Reviews загружены')


def load_comments():
    with open(
        os.path.join(DATA_DIR, 'comments.csv'),
        newline='',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            review = Review.objects.get(id=row['review_id'])
            Comment.objects.update_or_create(
                id=row['id'],
                defaults={
                    'review_id': row['review_id'],
                    'title_id': review.title_id,
                    'text': row['text'],
                    'author_id': row['author'],
                    'pub_date': row['pub_date']
                }
            )
    print('Comments загружены')


if __name__ == '__main__':
    load_category()
    load_genre()
    load_titles()
    load_genre_title()
    load_users()
    load_reviews()
    load_comments()
    print('Данные загружены')
