from rest_framework.permissions import BasePermission


class IsAnonymoused(BasePermission):
    message = 'permission denied, at first you must logout'
    """
    Allows access only to not authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)
