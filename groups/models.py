from django.db import models

from users.models import Profile


class Group(models.Model):
    """
        Model for representing Group entity
    """
    name = models.CharField(max_length=50,null=False)
    user = models.ManyToManyField(Profile, related_name='user_in_group')
    mentor = models.ManyToManyField(Profile, related_name='mentor_in_group')

    def __str__(self):
        return f'{self.name}'