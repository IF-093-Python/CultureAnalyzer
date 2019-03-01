from django.urls import path, re_path, include

from quiz.views import QuizzesList, CreateQuizView, \
    DeleteQuizView, UpdateQuizView, ResultsListView, QuizDetailView, \
    CurrentResultView

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
    path('quiz_detail/<int:pk>/', QuizDetailView.as_view(),
         name='detail-quiz'),
    re_path('^column_chart/(?P<pk>\\d+)/', include([
        path('', CurrentResultView.as_view(), name='result-chart'),
        re_path('^group=(?P<group>\\w+[\\s,-]*\\w*)/$',
                CurrentResultView.as_view(), name='result-chart-group'),
        re_path('^user=(?P<current_user>\\w+[\\s,-]*\\w*)/$',
                CurrentResultView.as_view(),name='result-chart-group'),

        ])),
]
