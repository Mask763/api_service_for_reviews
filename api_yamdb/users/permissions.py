from rest_framework import permissions

from .config import USER_ROLE_ADMIN, USER_ROLE_MODERATOR


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user.role == USER_ROLE_ADMIN
                or request.user.is_superuser
            )


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == USER_ROLE_ADMIN
                or request.user.is_superuser
            )
        )


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            ((obj.author == request.user) and (request.user.role == 'user'))
            or (request.user.role == 'moderator')
            or (request.user.role == 'admin')
        )


class IsAuthorOrAdministration(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.role == USER_ROLE_ADMIN
                or request.user.role == USER_ROLE_MODERATOR
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS
