from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (SignUpSerializer, FeedbackSerializer,
                             ProfileSerializer, TraineeQuizzesSerializer)
from feedbacks.models import Feedback
from quiz.models import Quizzes
from api.permissions import HasGroupPermission
from CultureAnalyzer.constants import MENTOR_ID

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet',
           'TraineeQuizzesView']


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
        'list': [MENTOR_ID],
        'create': [MENTOR_ID],
        'partial_update': [MENTOR_ID],
        'retrieve': [MENTOR_ID],
        'destroy': [MENTOR_ID],
        }


class TraineeQuizzesView(generics.ListAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = TraineeQuizzesSerializer
    filter_fields = ('title', 'description', 'type_of_quiz')
    search_fields = ('title', 'description', 'type_of_quiz')
