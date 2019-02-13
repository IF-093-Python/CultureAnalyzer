from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


TYPE_OF_QUIZ = ((1, 'Business'), (2, 'General'))


class Quizzes(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    type_of_quiz = models.IntegerField(choices=TYPE_OF_QUIZ, default=1)

    def __str__(self):
        return self.title


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = models.TextField('Description', null=False)

    def __str__(self):
        return self.user.username
