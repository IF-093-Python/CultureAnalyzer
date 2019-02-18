from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.choices import GENDER_CHOICES, EDUCATION_CHOICES


class CustomUser(AbstractUser):
    """
        date_of_birth, experience, gender and education are nullable
        in case we will use oauth2 and cannot automatically take this data

        user can change the data in profile page

        Django forms and serializer do not allow you to leave data empty.
        """
    image = models.ImageField(upload_to='profile_pics',
                              blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    experience = models.IntegerField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, null=True)
    education = models.CharField(choices=EDUCATION_CHOICES, max_length=50,
                                 null=True)

    def save(self, **kwargs):
        """
        if img is too big we decrease img
        because the less image is the less memory it takes
        """
        super(CustomUser, self).save(**kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username}'
