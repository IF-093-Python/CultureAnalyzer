from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


MAX_FIELD_REPRESENTATION = 20


class CountryIndicator(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    PDI = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    IND = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    MAS = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    UAI = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    LTO = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    IVR = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    class Meta:
        db_table = 'countries_indicators'

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
        return f'{self.name[:MAX_FIELD_REPRESENTATION]} - {self.iso_code}'

