from rest_framework import serializers

from quiz.models import Quizzes
from tutors.models import Questions, Answers

__all__ = ['TraineeQuizzesSerializer', 'TraineeQuestionsSerializer',
           'TraineeAnswersSerializer', 'MentorQuizSerializer',
           'MentorQuestionSerializer', 'MentorAnswerSerializer']


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


class MentorQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizzes
        fields = '__all__'


class MentorQuestionSerializer(serializers.ModelSerializer):
    quiz = MentorQuizSerializer

    class Meta:
        model = Questions
        fields = '__all__'


class MentorAnswerSerializer(serializers.ModelSerializer):
    question = MentorQuestionSerializer

    class Meta:
        model = Answers
        fields = '__all__'
