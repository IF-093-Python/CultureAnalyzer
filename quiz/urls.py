from django.urls import re_path, path

from quiz.views import QuizzesList, CreateQuizView, \
    DeleteQuizView, UpdateQuizView, ResultsListView
from . import views

app_name = "quiz"

urlpatterns = [
    path('quiz_list/', QuizzesList.as_view(), name='quizzes-list'),
    path('create_quiz/', CreateQuizView.as_view(), name='create-quiz'),
    re_path('^delete_quiz/(?P<pk>\\d+)$', DeleteQuizView.as_view(),
            name='delete-quiz'),
    re_path('^update_quiz/(?P<pk>\\d+)$', UpdateQuizView.as_view(),
            name='update-quiz'),
    path('result_list/', ResultsListView.as_view(),
         name='result-list'),
    path('column_chart/<int:pk>/', views.get_result_from,
         name='result-chart'),
]
