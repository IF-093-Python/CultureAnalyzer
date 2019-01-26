from PIL import Image
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
    image = models.ImageField(upload_to='profile_pics',
                              blank=True, null=True)

    def save(self, **kwargs):
        """
        if img is too big we decrease img
        because the less image is the less memory it takes
        """
        super(Profile, self).save(**kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} => {self.role.name}'

    class Meta:
        db_table = "profiles"
