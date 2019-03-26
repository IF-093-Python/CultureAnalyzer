from django.urls import path
from groups.views import (GroupsList, CreateGroupView, UpdateGroupView,
                          DeleteGroupView, MentorGroupsView, MentorGroupUpdate,
                          MentorGroupAdd,
                          AddNewUser, SheduleGroupListView, SheduleGroupView,
                          AddInvitation)

app_name = 'groups'

urlpatterns = [
    path('', GroupsList.as_view(),
         name='groups-list'),
    path('create-group/', CreateGroupView.as_view(),
         name='create-group'),
    path('delete-group/<int:pk>', DeleteGroupView.as_view(),
         name='delete-group'),
    path('update-group/<int:pk>', UpdateGroupView.as_view(),
         name='update-group'),
    path('mentor-groups/', MentorGroupsView.as_view(),
         name='mentor_groups_view'),
    path('group/<int:pk>/', MentorGroupUpdate.as_view(),
         name='mentor_group_update'),
    path('group/add/<int:pk>/', MentorGroupAdd.as_view(),
         name='mentor_group_add'),
    path('invite/<int:pk>/', AddInvitation.as_view(),
         name='add_invitation'),
    path('join/<str:hash>', AddNewUser.as_view(),
         name='add_new_user'),
    path('group/set_quiz/<int:pk>/', SheduleGroupView.as_view(),
         name='shedule_group'),
    path('group/quiz/<int:pk>/', SheduleGroupListView.as_view(),
         name='shedule_group_list'),

]
