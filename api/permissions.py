from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_customuser')


class CanChangeUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = obj
        if current_user.is_superuser or \
                not request.user.is_superuser and current_user.is_admin:
            return False
        return True
