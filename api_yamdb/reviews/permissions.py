from rest_framework import permissions

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)
    

class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'moderator')
    

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin')
