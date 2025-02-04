# Запрешенные имена пользователей
WRONG_USERNAMES = ('me',)

# Список возможных ролей
USER_ROLE_USER = 'user'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_ADMIN = 'admin'
USER_ROLES = (
    (USER_ROLE_USER, 'User'),
    (USER_ROLE_ADMIN, 'Admin'),
    (USER_ROLE_MODERATOR, 'Moderator'),
)

# Список различных констант
MAX_CHARFIELD_LENGTH = 150
MAX_EMAIL_LENGTH = 254
