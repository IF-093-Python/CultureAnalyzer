from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, viewsets
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   RetrieveModelMixin, ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsAdmin, CanChangeUser, HasGroupPermission
from api.serializers import (SignUpSerializer, FeedbackSerializer,
                             ProfileSerializer, BlockProfileSerializer,
                             AdminListSerializer, TraineeQuizzesSerializer,
                             PermissionGroupSerializer)
from feedbacks.models import Feedback
from quiz.models import Quizzes
from CultureAnalyzer.constants import MENTOR_ID
from users.filters import admin_search

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet',
           'TraineeQuizzesView', 'GroupViewSet',
           'AdminListView']


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


class AdminListView(generics.ListAPIView):
    model = get_user_model()
    serializer_class = AdminListSerializer
    permission_classes = (IsAdmin,)
    filter_fields = ('is_active',)
    search_fields = ('username',)

    def get_queryset(self):
        return admin_search(self.request).qs


class BlockProfileView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    serializer_class = BlockProfileSerializer
    permission_classes = (IsAdmin, CanChangeUser)

    def get_queryset(self):
        return get_user_model().objects.all()


class TraineeQuizzesView(generics.ListAPIView):
    queryset = Quizzes.objects.all()
    serializer_class = TraineeQuizzesSerializer
    filter_fields = ('title', 'description', 'type_of_quiz')
    search_fields = ('title', 'description', 'type_of_quiz')


class GroupViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                   ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = PermissionGroupSerializer
