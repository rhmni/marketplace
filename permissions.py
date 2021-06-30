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


class IsSeller(BasePermission):
    """
        Allow access only user that is seller
    """

    message = 'permission denied, you are not seller user'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return bool(obj.is_seller)


class IsSellerAndHasStore(BasePermission):
    """
        Allow access only user that is seller and have store
    """

    message = "permission denied, you are not seller user or don't have store"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        has_store = True
        try:
            obj.store
        except:
            has_store = False
        return bool(obj.is_seller and has_store)


class IsSellerOfProduct(BasePermission):
    """
        Allow access only user that seller of product
    """

    message = 'permission denied, you are not seller of this product'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return bool(obj.seller.founder == request.user and request.user.is_seller)
