from django.contrib import admin
from .models import CountryIndicator


@admin.register(CountryIndicator)
class CountryIndicatorAdmin(admin.ModelAdmin):
    fields = ['__all__']
