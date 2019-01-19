from django.urls import path
from .views import QuestionListView, CreateQuestionView, DeleteQuestionView

urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('create_question/', CreateQuestionView.as_view(),
         name='create_question'),
    path('<int:pk>/delete_question/', DeleteQuestionView.as_view(),
         name='delete_question'),
]
