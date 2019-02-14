from django.urls import path, re_path
from .views import TestPlayer, index
from . import views

app_name = 'test_player'

urlpatterns = [
    path('', views.index, name='test_player'),
    re_path(r'^(?P<quiz_id>[0-9]+)/(?P<question_number>[0-9]+)/',
            TestPlayer.as_view(), name='player'),
]
