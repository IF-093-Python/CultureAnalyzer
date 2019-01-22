from django.urls import path
from .views import CategoryListView, CreateCategoryView, \
    CreateQuestionView, DeleteQuestionView, UpdateQuestionView, \
    CreateAnswerView

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories_list'),
    path('create_category/', CreateCategoryView.as_view(),
         name='create_category'),

    path('<int:pk>/create_question/', CreateQuestionView.as_view(),
         name='create_question'),

    path('<int:pk>/delete_question/', DeleteQuestionView.as_view(),
         name='delete_question'),
    path('<int:pk>/update_question/', UpdateQuestionView.as_view(),
         name='update_question'),
    path('<int:question_id>/create_answer/', CreateAnswerView.as_view(),
         name='create_answer'),
]
