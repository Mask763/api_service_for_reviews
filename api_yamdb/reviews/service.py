from datetime import datetime

from rest_framework import serializers


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise serializers.ValidationError(
            'Неверно введён год!'
        )
    return value
