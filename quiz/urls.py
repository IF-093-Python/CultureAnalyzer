from django.conf.urls import url
from django.urls import include
from quiz.views import QuizzesList


urlpatterns = [
    url(r'quizzes/', QuizzesList.as_view(), name='quizzes'),

]
