from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, viewsets
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   RetrieveModelMixin, ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers.account import SignUpSerializer, ProfileSerializer
from api.serializers.country_indicator import CountryIndicatorSerializer
from api.serializers.feedback import FeedbackSerializer
from api.serializers.permissions_group import PermissionGroupSerializer
from api.serializers.quiz import (MentorQuizSerializer,
                                  MentorQuestionSerializer,
                                  MentorAnswerSerializer,
                                  TraineeQuizzesSerializer)
from feedbacks.models import Feedback
from indicators.models import CountryIndicator
from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet',
           'TraineeQuizzesView', 'GroupViewSet', 'CountryIndicatorViewSet',
           'MentorQuizViewSet', 'MentorQuestionViewSet', 'MentorAnswerViewSet']


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
    serializer_class = PermissionGroupSerializer


class CountryIndicatorViewSet(viewsets.ModelViewSet):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer
    filter_fields = ('pdi', 'idv', 'mas', 'uai', 'lto', 'ivr')
    search_fields = ('iso_code', 'name')


class MentorQuizViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all()
    serializer_class = MentorQuizSerializer
    filter_fields = ('id', 'title', 'description', 'type_of_quiz')
    search_fields = ('id', 'title', 'description', 'type_of_quiz')


class MentorQuestionViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = MentorQuestionSerializer
    filterset_fields = (
        'quiz__id', 'quiz__title', 'quiz__type_of_quiz', 'question_number')
    search_fields = {
        'question_number': ('exact',),
        'question_text': ('icontains',)}


class MentorAnswerViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = MentorAnswerSerializer
    filter_fields = ('question__id', 'question__id',
                     'question__question_number' 'answer_number',)
    search_fields = {'answer_text': 'icontains'}
