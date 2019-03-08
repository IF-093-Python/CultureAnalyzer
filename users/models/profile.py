from PIL import Image
from django.db import models
from django.db.transaction import atomic

from users.choices import GENDER_CHOICES, EDUCATION_CHOICES
# import CustomUser instead of get_user_model because CustomUser
# is not initialized yet and get_user_model cannot return CustomUser
from users.models.custom_user import CustomUser
from users.validators import PValidationError

__all__ = ['Profile', 'Role']


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "roles"


class Profile(models.Model):
    """
    date_of_birth, experience, gender and education are nullable
    in case we will use oauth2 and cannot automatically take this data

    user can change the data in profile page

    Django forms and serializer do not allow you to leave data empty.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                db_column='user_id')
    role = models.ForeignKey(Role, on_delete=models.PROTECT,
                             db_column='role_id')
    image = models.ImageField(upload_to='profile_pics',
                              blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    experience = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, null=True)
    education = models.CharField(choices=EDUCATION_CHOICES, max_length=50,
                                 null=True)

    def __str__(self):
        return f'{self.user.username} => {self.role.name}'

    class Meta:
        db_table = "profiles"
