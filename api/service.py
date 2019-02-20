from abc import ABC, abstractmethod
from django.db import models
from django.db.models import Q, QuerySet, Manager

from api.permissions import is_mentor, is_admin, is_superadmin, is_trainee
from users.models.custom_user import CustomUser

__all__ = ['UserService']


class AbstractQuerysetFactory(ABC):
    def __init__(self, user: CustomUser) -> None:
        super().__init__()
        self.user = user

    @property
    def model(self) -> models.Model:
        return NotImplementedError()

    def query(self) -> Manager:
        return self.model.objects

    def get_superadmin_queryset(self) -> QuerySet:
        return self.query().all()

    def get_admin_queryset(self) -> QuerySet:
        return self.query().filter(self.admin_predicate())

    def get_mentor_queryset(self) -> QuerySet:
        return self.query().filter(self.mentor_predicate())

    def get_trainee_queryset(self) -> QuerySet:
        return self.query().filter(self.trainee_predicate())

    @abstractmethod
    def admin_predicate(self) -> Q:
        raise NotImplementedError()

    @abstractmethod
    def mentor_predicate(self) -> Q:
        raise NotImplementedError()

    @abstractmethod
    def trainee_predicate(self) -> Q:
        raise NotImplementedError()

    def get_queryset_by_role(self) -> QuerySet:
        queryset = self.query().none()
        if is_superadmin(self.user):
            queryset = self.get_superadmin_queryset()
        elif is_admin(self.user):
            queryset = self.get_admin_queryset()
        elif is_mentor(self.user):
            queryset = self.get_mentor_queryset()
        elif is_trainee(self.user):
            queryset = self.get_trainee_queryset()
        return queryset


class UserService(AbstractQuerysetFactory):
    model = CustomUser

    def admin_predicate(self) -> Q:
        return all_without_admins(self.user)

    def mentor_predicate(self) -> Q:
        return all_trainees(self.user)

    def trainee_predicate(self) -> Q:
        return this_user(self.user)


def all_without_admins(user: CustomUser) -> Q:
    without_superadmin = ~Q(id=1)
    without_admins = ~Q(is_superuser=True)
    self_user = this_user(user)
    return (without_superadmin & without_admins) | self_user


def all_trainees(user: CustomUser) -> Q:
    trainees = Q(is_staff=False)
    self_user = this_user(user)
    return trainees | self_user


def this_user(user: CustomUser) -> Q:
    return Q(id=user.id)
