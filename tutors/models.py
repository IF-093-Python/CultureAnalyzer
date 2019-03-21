from django.db import models

from quiz.models import Quizzes

__all__ = ['Questions', 'Answers', ]


class Questions(models.Model):
    """
    Model Question have the field 'question_number', that indicates the issue
    number in a particular quiz.
    """
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, null=False)
    question_number = models.IntegerField(null=False)
    question_text = models.TextField(null=False)

    def __str__(self):
        return self.question_text

    class Meta:
        """
        The tuple of the fields 'quiz' and 'question_number', which should be
        unique together.
        """
        unique_together = (('quiz', 'question_number'),)


class Answers(models.Model):
    """
     Model Answer have the field 'answer_number', that indicates the issue
     number in a particular question and is responsible for scores.
     """
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,
                                 null=False)
    answer_number = models.IntegerField(null=False)
    answer_text = models.TextField(null=False)

    def __str__(self):
        return self.answer_text

    class Meta:
        """
        The tuple of the fields 'question' and 'answer_text', which should be
        unique together.
        """
        unique_together = (('question', 'answer_text'),)
