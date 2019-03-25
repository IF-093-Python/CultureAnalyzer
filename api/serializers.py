from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from CultureAnalyzer.exceptions import FValidationError
from api.fields import PasswordField, UniqueEmailField
from feedbacks.models import Feedback
from feedbacks.validator import FeedbackValidator
from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = ['SignUpSerializer', 'ProfileSerializer', 'FeedbackSerializer',
           'TraineeQuizzesSerializer', 'PermissionGroupSerializer']


class AccountSerializer(serializers.ModelSerializer):
    password = PasswordField()
    email = UniqueEmailField()

    @property
    def validated_data(self):
        validated_data = super().validated_data
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return validated_data


class SignUpSerializer(AccountSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name')


class ProfileSerializer(AccountSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name',
                  'date_of_birth', 'experience', 'gender', 'education',
                  'image')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'feedback', 'min_value', 'max_value', 'indicator')

    def validate(self, data):
        try:
            FeedbackValidator.validate_min_value(data)
        except FValidationError as err:
            raise serializers.ValidationError({'min_value': str(err)})
        return data


class TraineeAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('answer_number', 'answer_text')


class TraineeQuestionsSerializer(serializers.ModelSerializer):
    answers = TraineeAnswersSerializer(many=True, source='answers_set')

    class Meta:
        model = Questions
        fields = ('question_number', 'question_text', 'answers')


class TraineeQuizzesSerializer(serializers.ModelSerializer):
    questions = TraineeQuestionsSerializer(many=True, source='questions_set')

    class Meta:
        model = Quizzes
        fields = ('title', 'description', 'type_of_quiz', 'questions')


class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
