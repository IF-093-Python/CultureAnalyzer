from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers.account import (SignUpSerializer, ProfileSerializer)
from api.serializers.country_indicator import CountryIndicatorSerializer
from api.serializers.feedback import FeedbackSerializer
from api.serializers.quiz import (TraineeQuizzesSerializer,
                                  MentorQuizSerializer, MentorAnswerSerializer,
                                  MentorQuestionSerializer)
from feedbacks.models import Feedback
from indicators.models import CountryIndicator
from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet',
           'TraineeQuizzesView', 'CountryIndicatorViewSet',
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


class CountryIndicatorViewSet(viewsets.ModelViewSet):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer
    filter_fields = (
        'iso_code', 'name', 'pdi', 'idv', 'mas', 'uai', 'lto', 'ivr')
    search_fields = (
        'iso_code', 'name', 'pdi', 'idv', 'mas', 'uai', 'lto', 'ivr')


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
