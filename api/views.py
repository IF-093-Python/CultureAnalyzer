from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from api.serializers import SignUpSerializer, FeedbackSerializer
from feedbacks.models import Feedback

__all__ = ['SignUpView']


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
