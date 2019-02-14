from django.urls import path, re_path
from .views import TestPlayer, TestStart

app_name = 'test_player'

urlpatterns = [
    path('', TestStart.as_view(), name='start_test'),
    re_path(r'^(?P<quiz_id>[0-9]+)/(?P<question_number>[0-9]+)/',
            TestPlayer.as_view(), name='test_player'),
]
