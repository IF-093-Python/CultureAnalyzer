from django.contrib import admin

from indicators.models import CountryIndicator


@admin.register(CountryIndicator)
class CountryIndicatorAdmin(admin.ModelAdmin):
    fields = ['iso_code', 'name', 'pdi', 'ind', 'mas', 'uai', 'lto', 'ivr']
