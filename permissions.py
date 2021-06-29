from rest_framework.permissions import BasePermission


class IsAnonymoused(BasePermission):
    """
    Allows access only to not authenticated users.
    """

    message = 'permission denied, at first you must logout'

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)


class IsOwnerOfTicket(BasePermission):
    """
    Allow access only user that owner of ticket
    """

    message = 'permission denied, you are not owner of this ticket'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
