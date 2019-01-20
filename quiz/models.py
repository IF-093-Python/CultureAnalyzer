from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import SET_NULL, CASCADE


class Quizzes(models.Model):
    """
    Model for representing Quiz entity
    """
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)

    def __str__(self):
        """
        String for representing the Model object (in Admin site for example)
        """
        return self.title


class Results(models.Model):
    """
    Model for representing Result entity
    """
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = models.TextField('Description', null=False)

    def __str__(self):
        """
        String for representing the Model object (in Admin site for example)
        """
        return self.user.username
