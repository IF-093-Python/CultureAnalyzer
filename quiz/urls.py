from django.urls import include, re_path
from quiz.views import QuizzesList, CreateQuizView, \
    DeleteQuizView, UpdateQuizView
app_name = "quiz"

urlpatterns = [
    re_path('^quiz_list/$', QuizzesList.as_view(), name='quizzes-list'),
    re_path('^create_quiz/$', CreateQuizView.as_view(), name='create-quiz'),
    re_path('^delete_quiz/(?P<pk>\\d+)$', DeleteQuizView.as_view(),
            name='delete-quiz'),
    re_path('^update_quiz/(?P<pk>\\d+)$', UpdateQuizView.as_view(),
            name='update-quiz'),

]
