from django.urls import path
from .views import CategoryListView, CreateCategoryView, DeleteCategoryView,\
    QuestionListView, CreateQuestionView, DeleteQuestionView, \
    UpdateQuestionView

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories_list'),
    path('create_category/', CreateCategoryView.as_view(),
         name='create_category'),
    path('<int:pk>/delete_category/', DeleteCategoryView.as_view(),
         name='delete_category'),

    path('<int:category_id>/questions_list/', QuestionListView.as_view(),
         name='questions_list'),
    path('<int:category_id>/create_question/', CreateQuestionView.as_view(),
         name='create_question'),
    path('<int:pk>/delete_question/',
         DeleteQuestionView.as_view(), name='delete_question'),
    path('<int:pk>/update_question/',
         UpdateQuestionView.as_view(), name='update_question'),

]
