from django.urls import path

from .views import CreateQuestionView, UpdateQuestionView, \
    DeleteQuestionView, AnswerListView, CreateAnswerView, UpdateAnswerView, \
    DeleteAnswerView

app_name = 'tutors'

urlpatterns = [
    path('<int:quiz_id>/create_question/', CreateQuestionView.as_view(),
         name='create_question'),
    path('<int:quiz_id>/update_question/<int:pk>/',
         UpdateQuestionView.as_view(), name='update_question'),
    path('<int:quiz_id>/delete_question/<int:pk>/',
         DeleteQuestionView.as_view(), name='delete_question'),
    path('<int:question_id>/answers_list/', AnswerListView.as_view(),
         name='answers_list'),
    path('<int:question_id>/create_answer/', CreateAnswerView.as_view(),
         name='create_answer'),
    path('<int:question_id>/update_answer/<int:pk>',
         UpdateAnswerView.as_view(), name='update_answer'),
    path('<int:pk>/delete_answer/', DeleteAnswerView.as_view(),
         name='delete_answer'),
]
