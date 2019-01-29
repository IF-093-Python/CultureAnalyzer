from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse


class Feedback(models.Model):
    INDICATORS = (
        ('PDI', 'PDI'),
        ('IND', 'IND'),
        ('MAS', 'MAS'),
        ('UAI', 'UAI'),
        ('LTO', 'LTO'),
        ('IVR', 'IVR'),
    )

    feedback = models.TextField()
    min_value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    max_value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    indicator = models.CharField(max_length=3, choices=INDICATORS, default='PDI')

    class Meta:
        db_table = 'Feedbacks'

    def get_absolute_url(self):
        return reverse('feedback-list')

    def __str__(self):
        return f'Feedback - {self.feedback}'
