from django.contrib import admin
from .models import CountryIndicator


@admin.register(CountryIndicator)
class CountryIndicatorAdmin(admin.ModelAdmin):
    fields = ['iso_code', 'name', 'PDI', 'IND', 'MAS', 'UAI', 'LTO', 'IVR']
