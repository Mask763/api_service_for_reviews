from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


# class IsAuthorOrAdminisration(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.role in ('moderator', 'admin')
#             or request.user.is_superuser
#         )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)


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
