from django.db import models
from django.core.exceptions import ValidationError


class CountryIndicator(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    PDI = models.SmallIntegerField()
    IND = models.SmallIntegerField()
    MAS = models.SmallIntegerField()
    UAI = models.SmallIntegerField()
    LTO = models.SmallIntegerField()
    IVR = models.SmallIntegerField()

    class Meta:
        db_table = 'CountriesIndicators'

    def clean(self):
        """Validate iso_code on case sensitive value.
           Example: can't be codes 'ukr' and 'Ukr' or 'UKR' at
           same time."""
        if CountryIndicator.objects.filter(iso_code__iexact=self.iso_code)\
                                   .count() > 0:
            raise ValidationError(f'Code: {self.iso_code} already exists.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CountryIndicator, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name[:20]} - {self.iso_code}'


class Feedback(models.Model):
    feedback = models.TextField()

    class Meta:
        db_table = 'Feedbacks'

    def __str__(self):
        return f'Feedback - {self.feedback[:20]}'
