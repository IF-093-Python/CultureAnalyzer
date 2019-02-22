from rest_framework.permissions import BasePermission

from users.models import CustomUser

__all__ = ['UserPermission', 'is_superadmin', 'is_admin', 'is_mentor',
           'is_trainee']


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return is_superadmin(user) or is_admin(user) or is_mentor(user)

    def has_object_permission(self, request, view, obj):
        return is_superadmin(request.user) or is_admin(request.user)


class IsTrainee(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.id == request.user.id
        return is_owner


def is_superadmin(user: CustomUser) -> bool:
    superadmin_id = 1
    return user.id == superadmin_id


def is_admin(user: CustomUser) -> bool:
    return user.is_superuser


def is_mentor(user: CustomUser) -> bool:
    return user.is_staff and not user.is_superuser


def is_trainee(user: CustomUser) -> bool:
    return not user.is_staff
