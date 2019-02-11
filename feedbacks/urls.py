from django.urls import path

from feedbacks.views import *
from feedbacks.api_views import *

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback-list'),
    path('<int:pk>', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('delete/<int:pk>', FeedbackDeleteView.as_view(),
         name='feedback-delete'),
    path('create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('update/<int:pk>', FeedbackUpdateView.as_view(),
         name='feedback-update'),
    path('recommendation/delete/<int:pk>', RecommendationDeleteView.as_view(),
         name='recommendation-delete'),
    path('recommendation/create/',
         RecommendationCreateView.as_view(),
         name='recommendation-create'),
    path('recommendation/update/<int:pk>', RecommendationUpdateView.as_view(),
         name='recommendation-update'),
    path('api/feedbacks', FeedbackList.as_view()),
    path('api/feedbacks/<int:pk>', FeedbackDetail.as_view()),
    path('api/recommendations', RecommendationList.as_view()),
    path('api/recommendations/<int:pk>', RecommendationDetail.as_view())
]
