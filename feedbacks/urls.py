from django.urls import path

from .views import FeedbackListView, FeedbackCreateView, FeedbackDeleteView, \
    FeedbackUpdateView

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback-list'),
    path('delete/<int:pk>', FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('update/<int:pk>', FeedbackUpdateView.as_view(), name='feedback-update'),
]
