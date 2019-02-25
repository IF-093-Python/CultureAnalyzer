from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm
from .views import UserRegisterView, ListGroups, UpdateGroups, DeleteGroups, \
    CreateGroup

__all__ = ['urlpatterns']

urlpatterns = [
    path('', TemplateView.as_view(template_name='users/index.html'),
         name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('admin_page/', views.AdminListView.as_view(), name='admin'),
    path('login/', views.LoginView.as_view(
        template_name='users/login.html', authentication_form=UserLoginForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('profile/<int:pk>', views.UserUpdateView.as_view(), name='profile'),
    path('profile/<int:pk>/password_change', views.PasswordChangeView.as_view()
         , name='password-change'),
    path('login/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('login/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    re_path(
        'login/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('login/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('admin_page/update/<int:pk>', views.ProfileUpdateView.as_view(),
         name='change-profile'),

    path('group_page/', ListGroups.as_view(), name='group_perm-list'),
    path('update_group/<int:pk>', UpdateGroups.as_view(),
         name='group_perm-update'),
    path('delete_group/<int:pk>', DeleteGroups.as_view(),
         name='group_perm-delete'),
    path('create_group', CreateGroup.as_view(), name='group_perm-create'),
    ]
