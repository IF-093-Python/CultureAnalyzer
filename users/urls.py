from django.urls import path
from . import views
from .views import UserRegisterView

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', UserRegisterView.as_view(), name='register')

]