from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from feedbacks.models import Feedback, Recommendation
from feedbacks.serializers import FeedbackSerializer, RecommendationSerializer


@api_view(['GET'])
def protected_view(request):
    return Response({'username': f'{request.user.username}'})


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class RecommendationList(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer


class RecommendationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
