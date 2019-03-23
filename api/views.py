from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

from api.serializers import SignUpSerializer, FeedbackSerializer, \
    ProfileSerializer
from api.permissions import HasGroupPermission
from feedbacks.models import Feedback
from CultureAnalyzer.constants import TRAINEE_ID, MENTOR_ID, ADMIN_ID

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet']


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class ProfileView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    permission_classes = [HasGroupPermission]
    permission_groups = {
        'list': [MENTOR_ID, TRAINEE_ID],
        'create': [MENTOR_ID],
        'partial_update': [MENTOR_ID],
        'retrieve': [MENTOR_ID],
        'destroy': [ADMIN_ID],
        }
