from django.db import models
#from quizzs.models import Quizz

class Question(models.Model):
    #quizz = models.ManyToManyField(Quizz, on_delete=models.CASCADE, db_column='quizz_id')
    question_text = models.CharField(max_length=100, null=False)

    def _str_(self):
        return f'{self.question_text[:20]}'

    class Meta:
        db_table = "Questions"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='answer_id')
    answer_text = models.CharField(max_length=100, null=False)

    def _str_(self):
        return f'{self.Question.question_text[:10]}: {self.answer_text[:20]}'

    class Meta:
        db_table = "Answers"
