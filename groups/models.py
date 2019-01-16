from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'
