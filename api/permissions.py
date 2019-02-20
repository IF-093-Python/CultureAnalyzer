from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import CustomUser

__all__ = ['IsSuperAdmin', 'IsAdmin', 'IsMentor', 'IsTrainee',
           'is_superadmin', 'is_admin', 'is_mentor', 'is_trainee']


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsSuperAdmin(IsAdmin):
    pass


class IsMentor(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.id == request.user.id
        if request.method in SAFE_METHODS or is_owner:
            return True
        return False


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
