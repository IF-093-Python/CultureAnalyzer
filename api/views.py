from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, viewsets
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, \
    RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers import (SignUpSerializer, FeedbackSerializer,
                             ProfileSerializer, TraineeQuizzesSerializer,
                             PermissionGroup)
from feedbacks.models import Feedback
from quiz.models import Quizzes

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet',
           'TraineeQuizzesView', 'GroupViewSet']


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


class TraineeQuizzesView(generics.ListAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = TraineeQuizzesSerializer
    filter_fields = ('title', 'description', 'type_of_quiz')
    search_fields = ('title', 'description', 'type_of_quiz')


class GroupViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                   ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = PermissionGroup
