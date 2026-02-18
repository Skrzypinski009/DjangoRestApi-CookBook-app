from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    For anyone: GET
    For author: PUT, PATCH, DELETE
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
