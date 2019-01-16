from django.db import models
from django.contrib.auth.models import User


class Roles(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.OneToOneField(Roles, on_delete=models.PROTECT)

    def __str__(self):
        return f'{user.username}'
