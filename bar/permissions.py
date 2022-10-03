from rest_framework.permissions import BasePermission, SAFE_METHODS


class BarPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class ReferencesPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class OrderPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return not request.user.is_authenticated
        if request.method == 'GET':
            return request.user.is_authenticated
