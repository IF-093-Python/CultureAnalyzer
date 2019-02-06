from django.db import models
from quiz.models import Quizzes


class Questions(models.Model):
    """
    Model Question have the field 'title', that indicates the issue number
    in a particular quiz.
    """
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, null=False)
    title = models.IntegerField(null=False)
    question_text = models.TextField(null=False)

    def __str__(self):
        return self.question_text

    class Meta:
        """
        The tuple of the fields 'quiz' and 'title', which should be
        unique together.
        """
        unique_together = (('quiz', 'title'),)


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,
                                 null=False)
    answer_text = models.TextField(null=False)

    def __str__(self):
        return self.answer_text

    class Meta:
        """
        The tuple of the fields 'question' and 'answer_text', which should be
        unique together.
        """
        unique_together = (('question', 'answer_text'),)
