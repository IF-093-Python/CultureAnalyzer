from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinLengthValidator


MAX_FIELD_REPRESENTATION = 20


class CountryIndicator(models.Model):
    iso_code = models.CharField(max_length=3, primary_key=True,
                                validators=[MinLengthValidator(3)])
    name = models.CharField(max_length=50, unique=True)
    PDI = models.PositiveIntegerField()
    IND = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    MAS = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    UAI = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    LTO = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    IVR = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    class Meta:
        db_table = 'countries_indicators'
        ordering = ['iso_code', 'name']
        verbose_name_plural = 'countries\' indicators'

    def clean(self):
        """Validate iso_code on case sensitive value.
           Example: can't be codes 'ukr' and 'Ukr' or 'UKR' at
           same time."""
        if CountryIndicator.objects.filter(iso_code__iexact=self.iso_code)\
                                   .count() > 0:
            raise ValidationError(f'Code: {self.iso_code} already exists.')

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        self.full_clean()  # validate clean when save is called
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name[:MAX_FIELD_REPRESENTATION]} - {self.iso_code}'

