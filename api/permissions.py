from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_customuser')


class CanChangeUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        selected_user = obj
        if selected_user.is_superuser or \
                not request.user.is_superuser and selected_user.is_admin:
            return False
        return True
