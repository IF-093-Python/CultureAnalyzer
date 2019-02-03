from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,\
                                   MinLengthValidator, MaxLengthValidator


MAX_FIELD_REPRESENTATION = 20


class CountryIndicator(models.Model):
    iso_code = models.CharField(max_length=3, unique=True,
                                validators=[MinLengthValidator(3),
                                            MaxLengthValidator(3)])
    name = models.CharField(max_length=200, unique=True)
    pdi = models.PositiveIntegerField(verbose_name='PDI',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    ind = models.PositiveIntegerField(verbose_name='IND',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    mas = models.PositiveIntegerField(verbose_name='MAS',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    uai = models.PositiveIntegerField(verbose_name='UAI',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    lto = models.PositiveIntegerField(verbose_name='LTO',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])
    ivr = models.PositiveIntegerField(verbose_name='IVR',
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(100)])

    class Meta:
        db_table = 'countries_indicators'
        ordering = ['iso_code', 'name']
        verbose_name_plural = 'countries\' indicators'

    def __str__(self):
        return f'{self.name[:MAX_FIELD_REPRESENTATION]} - {self.iso_code}'

