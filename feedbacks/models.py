from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

__all__ = ['Feedback', 'Recommendation', ]


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
    min_value = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)])
    max_value = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)])
    indicator = models.CharField(max_length=3, choices=INDICATORS,
                                 default='PDI')

    class Meta:
        db_table = 'Feedbacks'
        unique_together = ('min_value', 'max_value', 'indicator',)

    def get_absolute_url(self):
        return reverse('feedback-detail', args=[self.pk])

    def __str__(self):
        return self.feedback[:30]


class Recommendation(models.Model):
    recommendation = models.TextField()
    feedback = models.ForeignKey('Feedback', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('feedback-detail', args=[self.feedback.pk])

    def __str__(self):
        return self.recommendation[:30]
