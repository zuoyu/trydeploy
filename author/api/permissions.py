from rest_framework import permissions


class IsAdminOrSelfOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj == request.user or
            request.user.is_superuser
        )
