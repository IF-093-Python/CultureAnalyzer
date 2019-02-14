from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from feedbacks.models import Feedback, Recommendation
from feedbacks.serializers import FeedbackSerializer, RecommendationSerializer
from indicators.models import CountryIndicator
from indicators.serializers import CountryIndicatorSerializer


@api_view(['GET'])
def protected_view(request):
    return Response({'username': f'{request.user.username}'})


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_fields = ('indicator', )
    search_fields = ('feedback', )


class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class RecommendationList(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    search_fields = ('recommendation', )


class RecommendationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer


class CountryIndicatorList(generics.ListCreateAPIView):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer


class CountryIndicatorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer
