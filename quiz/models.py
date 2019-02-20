from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import CASCADE

TYPE_OF_QUIZ = (('Business', 'Business'), ('General', 'General'))

from users.models import CustomUser


class Quizzes(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    type_of_quiz = models.CharField(choices=TYPE_OF_QUIZ, max_length=20)

    def __str__(self):
        return self.title


class Results(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=CASCADE, null=False)
    pass_date = models.DateTimeField(null=False)
    result = JSONField()

    def __str__(self):
        return self.user.username

