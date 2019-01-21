from django.urls import path
from .views import *

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback-list'),
    path('delete/<int:pk>', FeedbackDeleteView.as_view(), name='feedback-delete'),
]
