from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    # Business upload permissions are only allowed for business owners. Allow all users to read.
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsClient(permissions.BasePermission):
    # Business upload permissions are only allowed for Business owners. Allow all users to read.
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client is True


class IsStaff(permissions.BasePermission):
    # Simple Business upload permissions are only allowed for Registered Staff. Allow all users to read.
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff is True
