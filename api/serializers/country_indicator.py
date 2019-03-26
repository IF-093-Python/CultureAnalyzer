from rest_framework import serializers

from indicators.models import CountryIndicator

__all__ = ['CountryIndicatorSerializer']


class CountryIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryIndicator
        fields = '__all__'
