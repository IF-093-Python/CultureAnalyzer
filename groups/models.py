from django.db import models

from users.models import CustomUser
from quiz.models import Quizzes

__all__ = ['Group', 'Shedule', ]


class Group(models.Model):
    """
        Model for representing Group entity
    """
    name = models.CharField(max_length=50, null=False)
    user = models.ManyToManyField(CustomUser, related_name='user_in_group')
    mentor = models.ManyToManyField(CustomUser, related_name='mentor_in_group')

    def __str__(self):
        return f'{self.name}'


class Shedule(models.Model):
    """
        Model for setting date and time for passing Quiz for Group
    """
    begin = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group} - {self.quiz}'
