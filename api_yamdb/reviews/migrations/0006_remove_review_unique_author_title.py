# Generated by Django 3.2 on 2024-06-24 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_title_options'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_title',
        ),
    ]
