from rest_framework import permissions


class IsAuthorOrModeratorOrAdmin(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            ((obj.author == request.user) and (request.user.role == 'user'))
            or (request.user.role == 'moderator')
            or (request.user.role == 'admin')
        )
