from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'
