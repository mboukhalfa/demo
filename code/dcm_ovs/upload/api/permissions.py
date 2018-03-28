from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow admins only.
    """

    def has_object_permission(self, request, view, obj):

        return request.user.is_staff