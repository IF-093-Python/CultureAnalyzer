from PIL import Image
from django.contrib.auth.models import AbstractUser, Group
from django.db import models, transaction

from CultureAnalyzer.constants import ADMIN_ID, TRAINEE_ID, MENTOR_ID
from users.choices import GENDER_CHOICES, EDUCATION_CHOICES

MAX_IMAGE_HEIGHT = 300
MAX_IMAGE_WIDTH = 300


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

    @property
    def is_admin(self):
        groups = Group.objects.get(pk=ADMIN_ID)
        return self in groups.user_set.all()

    @property
    def is_trainee(self):
        groups = Group.objects.get(pk=TRAINEE_ID)
        return self in groups.user_set.all()

    @property
    def is_mentor(self):
        groups = Group.objects.get(pk=MENTOR_ID)
        return self in groups.user_set.all()

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        if img is too big we decrease img
        because the less image is the less memory it takes
        """
        super(CustomUser, self).save(*args, **kwargs)
        try:
            if self.image:
                img = Image.open(self.image.path)
                if img.height > MAX_IMAGE_HEIGHT or img.width > MAX_IMAGE_WIDTH:
                    output_size = (MAX_IMAGE_HEIGHT, MAX_IMAGE_WIDTH)
                    img.thumbnail(output_size, Image.ANTIALIAS)
                    img.save(self.image.path)
        except (OSError, IOError):
            self.image = None
            super(CustomUser, self).save(update_fields=['image'])

    def __str__(self):
        return f'{self.username}'
