from django.contrib.auth.models import User, AnonymousUser
from rest_framework.permissions import BasePermission

SUPER_ADMIN_STR = 'Superadmin'
ADMIN_STR = 'Admin'
MENTOR_STR = 'Mentor'
TRAINEE_STR = 'Trainee'
ANON_STR = 'Anonymous'


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_superadmin(request.user)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return is_mentor(request.user)


class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return is_trainee(request.user)


def is_superadmin(user: User) -> bool:
    return user_role(user) == SUPER_ADMIN_STR


def is_admin(user: User) -> bool:
    return user_role(user) == ADMIN_STR


def is_mentor(user: User) -> bool:
    return user_role(user) == MENTOR_STR


def is_trainee(user: User) -> bool:
    return user_role(user) == TRAINEE_STR


def is_anonymous(user: User) -> bool:
    return isinstance(user, AnonymousUser)


def user_role(user: User) -> str:
    return ANON_STR if is_anonymous(user) else user.profile.role.name
