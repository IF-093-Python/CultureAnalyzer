from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from quiz.choices import TYPE_OF_QUIZ


class Quizzes(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    type_of_quiz = models.CharField(choices=TYPE_OF_QUIZ, default='Business',
                                    max_length=20)

    def __str__(self):
        return self.title


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = models.TextField('Description', null=False)

    def __str__(self):
        return self.user.username
