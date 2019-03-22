from django.urls import path

from quiz.views import (QuizzesList, CreateQuizView, QuizDetailView,
                        DeleteQuizView, UpdateQuizView, )

app_name = "quiz"

urlpatterns = [
    path('', QuizzesList.as_view(), name='quizzes-list'),
    path('create_quiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('quiz_detail/<int:pk>/', QuizDetailView.as_view(),
         name='detail-quiz'),
    path('delete_quiz/<int:pk>/', DeleteQuizView.as_view(),
         name='delete-quiz'),
    path('update_quiz/(<int:pk>/', UpdateQuizView.as_view(),
         name='update-quiz'),
]
