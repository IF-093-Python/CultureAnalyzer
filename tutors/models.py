from django.db import models
from quiz.models import Quizzes


class Questions(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=25, null=False, unique=True)
    question_text = models.TextField(null=False)

    def __str__(self):
        return self.question_text


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,
                                 null=False)
    answer_text = models.TextField(null=False)

    def __str__(self):
        return f'{self.question.title}: {self.answer_text}'
