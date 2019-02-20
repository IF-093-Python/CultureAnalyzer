from django.urls import path, re_path

from quiz.views import QuizzesList, CreateQuizView, \
    DeleteQuizView, UpdateQuizView, ResultsListView, QuizDetailView
from . import views

app_name = "quiz"

urlpatterns = [
    re_path('^quiz_list/$', QuizzesList.as_view(), name='quizzes-list'),
    re_path('^create_quiz/$', CreateQuizView.as_view(), name='create-quiz'),
    re_path('^delete_quiz/(?P<pk>\\d+)$', DeleteQuizView.as_view(),
            name='delete-quiz'),
    re_path('^update_quiz/(?P<pk>\\d+)$', UpdateQuizView.as_view(),
            name='update-quiz'),
    re_path('^result_list/(?P<user_id>\\d+)$', ResultsListView.as_view(),
            name='result-list'),
    path('column_chart/<int:pk>/', views.get_result_from,
         name='result-chart'),
    path('quiz_detail/<int:pk>/', QuizDetailView.as_view(),
         name='detail-quiz'),
]
