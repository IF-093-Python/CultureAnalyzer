from django.conf.urls import url
from django.urls import include
from quiz.views import QuizzesList, CreateQuizView


urlpatterns = [
    url('quiz_list', QuizzesList.as_view(), name='quizzes-list'),
    url(r'create_quiz/', CreateQuizView.as_view(), name='create-quiz'),

]
