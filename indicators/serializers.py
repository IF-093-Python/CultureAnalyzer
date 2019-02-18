from rest_framework import serializers

from indicators.models import CountryIndicator


class CountryIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryIndicator
        fields = '__all__'
