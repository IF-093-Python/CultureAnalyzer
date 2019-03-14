from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from users.choices import GENDER_CHOICES, EDUCATION_CHOICES

MIN_IMAGE_HEIGHT = 300
MIN_IMAGE_WIDTH = 300


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
    email = models.EmailField(blank=True, max_length=254,
                              verbose_name='email address', unique=True)

    @transaction.atomic
    def save(self, **kwargs):
        """
        if img is too big we decrease img
        because the less image is the less memory it takes
        """
        super(CustomUser, self).save(**kwargs)
        try:
            if self.image:
                img = Image.open(self.image.path)
                if img.height > MIN_IMAGE_HEIGHT or img.width > MIN_IMAGE_WIDTH:
                    output_size = (MIN_IMAGE_HEIGHT, MIN_IMAGE_WIDTH)
                    img.thumbnail(output_size, Image.ANTIALIAS)
                    img.save(self.image.path)
        except (OSError, IOError):
            self.image = None
            super(CustomUser, self).save(update_fields=['image'])

    def __str__(self):
        return f'{self.username}'
