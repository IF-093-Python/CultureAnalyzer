from django.urls import path
from groups.views import *

app_name = 'groups'

urlpatterns = [
    path('', GroupsList.as_view(), name='groups-list'),
    path('create_group/', CreateGroupView.as_view(), name='create-group'),
    path('delete_group/<int:pk>', DeleteGroupView.as_view(),
         name='delete-group'),
    path('update_group/<int:pk>', UpdateGroupView.as_view(),
         name='update-group'),

]
