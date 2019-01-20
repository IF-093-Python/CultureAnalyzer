from django.urls import path
from .views import QuestionListView, CreateQuestionView, DeleteQuestionView,\
    DetailQuestionView, UpdateQuestionView
urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('create_question/', CreateQuestionView.as_view(),
         name='create_question'),
    path('<int:pk>/delete_question/', DeleteQuestionView.as_view(),
         name='delete_question'),
    path('<int:pk>/detail_question/', DetailQuestionView.as_view(),
         name='detail_question'),
    path('<int:pk>/update_question/', UpdateQuestionView.as_view(),
         name='update_question'),
]
