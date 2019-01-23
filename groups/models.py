from django.contrib.auth.models import User
from django.db import models

from users.models import Profile


class Group(models.Model):
    """
        Model for representing Group entity
    """
    name = models.CharField(max_length=30)
    user = models.ManyToManyField(Profile)
    mentor = models.ManyToManyField(Profile)

    def __str__(self):
        return f'{self.name}'
