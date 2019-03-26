from django.urls import path, re_path, include

from quiz.views import (QuizzesList, CreateQuizView, QuizDetailView,
                        DeleteQuizView, UpdateQuizView, ResultView,
                        ResultsListView)

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
    path('result_list/<int:pk>/', ResultsListView.as_view(),
         name='result-list'),
    re_path('^column_chart/(?P<pk>\\d+)/', include([
        re_path('^group=(?P<group>\\w+.*\\w*)/$',
                ResultView.as_view(), name='result-chart-group'),
        re_path('^user=(?P<current_user>\\w+[\\s,-]*\\w*)/$',
                ResultView.as_view(), name='result-chart-user'),

        ])),
]
