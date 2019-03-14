from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

__all__ = ['Quizzes', 'Results']


class Quizzes(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    numbers_of_questions = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = models.TextField('Description', null=False)

    def __str__(self):
        return self.user.username
