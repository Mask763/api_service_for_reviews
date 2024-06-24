from rest_framework import permissions


class IsAdmin(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        return request.method in permissions.SAFE_METHODS
