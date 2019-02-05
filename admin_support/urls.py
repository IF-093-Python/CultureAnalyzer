from django.urls import path
from .views import *

app_name='admin_support'

urlpatterns = [
    path('', MentorGroupsView.as_view(), name='mentor_groups_view'),
    path('group/<int:pk>/', GroupView.as_view(),name='group_view')
]
