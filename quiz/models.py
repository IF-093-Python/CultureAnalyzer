from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import SET_NULL

from question.models import Questions


class Quizzes(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    question = models.ForeignKey(Questions, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site for example)
        """
        return self.name


class Results(models.Model):
    user_id = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    quiz_id = models.ForeignKey(Quizzes, on_delete=SET_NULL, null=True, blank=True)
    pass_date = models.DateTimeField()
    result = models.TextField()

    def __str__(self):
        """
        String for representing the Model object (in Admin site for example)
        """
        return self.user_id.username
