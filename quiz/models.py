from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import SET_NULL

from question.models import Questions


class Quizzes(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    question = models.ForeignKey(Questions, on_delete=SET_NULL, null=True)


class Results(models.Model):
    user_id = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    quiz_id = models.ForeignKey(Quizzes, on_delete=SET_NULL, null=True)
    pass_date = models.DateTimeField()
    result = models.TextField()
