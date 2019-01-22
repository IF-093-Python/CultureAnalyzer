from django.db import models
from django.urls import reverse


class Feedback(models.Model):
    feedback = models.TextField()

    class Meta:
        db_table = 'Feedbacks'

    def get_absolute_url(self):
        return reverse('feedback-list')

    def __str__(self):
        return f'Feedback - {self.feedback}'
