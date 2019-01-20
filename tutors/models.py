from django.db import models

from quiz.models import Quizzes


class Question(models.Model):
    quiz = models.ManyToManyField(Quizzes, db_column='quiz_id')
    question_text = models.CharField(max_length=100, null=False)

    def _str_(self):
        return f'{self.question_text[:20]}'

    class Meta:
        db_table = "Questions"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 db_column='answer_id')
    answer_text = models.CharField(max_length=100, null=False)

    def _str_(self):
        return f'{self.question.question_text[:10]}: {self.answer_text[:20]}'

    class Meta:
        db_table = "Answers"
