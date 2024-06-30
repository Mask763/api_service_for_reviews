from django.core.exceptions import ValidationError

from .constants import WRONG_USERNAMES


def validate_forbidden_username(value):
    """Проверка на запрещенные имена пользователей."""
    if value in WRONG_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {value} недопустимо.'
        )
