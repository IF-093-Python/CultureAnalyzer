from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from CultureAnalyzer.settings import LOGIN_URL, REGISTER_URL, LOGOUT_URL
from . import views
from .forms import UserLoginForm
from .views import UserRegisterView

__all__ = ['urlpatterns']

urlpatterns = [
    path('', views.index, name='home'),

    path('register/', UserRegisterView.as_view(), name=REGISTER_URL),

    path('login/',
         views.LoginView.as_view(
             template_name='users/login.html',
             authentication_form=UserLoginForm),
         name=LOGIN_URL),

    path('logout/', auth_views.LogoutView.as_view(), name=LOGOUT_URL),

    path('profile/<int:pk>', views.UserUpdateView.as_view(), name='profile'),

    path('profile/<int:pk>/password_change',
         views.PasswordChangeView.as_view(),
         name='password-change'),

    path('login/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_form.html'),
         name='password_reset'),

    path('login/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    re_path(
        "login/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/"
        "(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('login/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]
