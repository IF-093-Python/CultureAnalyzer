from django.contrib.auth.models import User
from django.db.models import Q
from typing import List

from api.permissions import (
    TRAINEE_STR,
    SUPER_ADMIN_STR,
    ADMIN_STR
)


def get_superadmin_users() -> List[User]:
    return User.objects.all()


def get_admin_users() -> List[User]:
    return User.objects.filter(
        ~Q(profile__role__name=ADMIN_STR) &
        ~Q(profile__role__name=SUPER_ADMIN_STR))


def get_mentor_users() -> List[User]:
    return User.objects.filter(profile__role__name=TRAINEE_STR)
