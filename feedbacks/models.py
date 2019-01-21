from django.db import models


class Feedback(models.Model):
    feedback = models.TextField()

    class Meta:
        db_table = 'Feedbacks'

    def __str__(self):
        return f'Feedback - {self.feedback}'
