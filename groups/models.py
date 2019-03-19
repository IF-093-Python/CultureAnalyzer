import uuid

from django.contrib.auth import get_user_model
from django.db import models

from quiz.models import Quizzes

__all__ = ['Group', 'Shedule', 'Invitation']


class Group(models.Model):
    """
        Model for representing Group entity
    """
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(get_user_model(), blank=True,
                                  related_name='user_in_group')
    mentor = models.ManyToManyField(get_user_model(), blank=True,
                                    related_name='mentor_in_group')

    class Meta:
        permissions = (
            ("view_mentor_group", "Can view mentor group"),
            ("change_mentor_group", "Can change mentor group"),
            ("add_mentor_group", "Can add mentor to group"),
        )

    def __str__(self):
        return f'{self.name}'


class Shedule(models.Model):
    """
        Model for setting date and time for passing Quiz for Group
    """
    begin = models.DateTimeField()
    end = models.DateTimeField()
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group} - {self.quiz}'


class Invitation(models.Model):
    """
        Model for saving generated URL for joining to group
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    items_left = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.code}'
