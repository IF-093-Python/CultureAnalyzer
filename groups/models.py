from django.contrib.auth import get_user_model
from django.db import models


class Group(models.Model):
    """
        Model for representing Group entity
    """
    name = models.CharField(max_length=30)
    user = models.ManyToManyField(get_user_model(),
                                  related_name='user_in_group')
    mentor = models.ManyToManyField(get_user_model(),
                                    related_name='mentor_in_group')

    def __str__(self):
        return f'{self.name}'
