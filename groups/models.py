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


class MyProfile(Profile):
    """
    Proxy Model for changing __str__ attribute of
    Profile model for proper representation
    of the name of user
    """
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} \
                ({self.user.username})'
