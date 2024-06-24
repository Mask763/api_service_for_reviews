# Generated by Django 3.2 on 2024-06-23 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_customuser_unique_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('moderator', 'Moderator')], default='user', max_length=10, verbose_name='Роль'),
        ),
    ]
