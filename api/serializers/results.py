from rest_framework import serializers

from quiz.models import Results


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


class CalculatedResultsSerializer(serializers.Serializer):
    pdi = serializers.IntegerField()
    idv = serializers.IntegerField()
    ivr = serializers.IntegerField()
    mas = serializers.IntegerField()
    uai = serializers.IntegerField()
    lto = serializers.IntegerField()

