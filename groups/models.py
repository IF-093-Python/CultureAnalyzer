from django.contrib.auth.models import User
from django.db import models

from users.models import Role


class Group(models.Model):
    name = models.CharField(max_length=30)
    user = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'
