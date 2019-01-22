from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "roles"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                db_column='user_id')
    role = models.ForeignKey(Role, on_delete=models.PROTECT,
                             db_column='role_id')

    def __str__(self):
        return f'{self.user.username} => {self.role.name}'

    class Meta:
        db_table = "profiles"
