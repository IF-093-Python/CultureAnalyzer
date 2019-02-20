from django.urls import path

from quiz.views import QuizzesList, CreateQuizView, \
    DeleteQuizView, UpdateQuizView, ResultsListView
from . import views

app_name = "quiz"

urlpatterns = [
    path('quiz_list/', QuizzesList.as_view(), name='quizzes-list'),
    path('create_quiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('delete_quiz/<int:pk>', DeleteQuizView.as_view(),
         name='delete-quiz'),
    path('update_quiz/<int:pk>', UpdateQuizView.as_view(),
         name='update-quiz'),
    path('result_list/', ResultsListView.as_view(),
         name='result-list'),
    path('column_chart/<int:pk>/', views.get_result_from,
         name='result-chart'),
]
