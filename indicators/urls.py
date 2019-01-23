from django.urls import path
from .views import *


app_name = 'country_indicator'


urlpatterns = [
    path('', CountryIndicatorListView.as_view(),
         name='country_indicator_list'),
    path('create/', CountryIndicatorCreate.as_view(),
         name='country_indicator_create'),
    path('<str:pk>/update/', country_indicator_update,
         name='country_indicator_update'),
    path('<str:pk>/delete/', CountryIndicatorDelete.as_view(),
         name='country_indicator_delete'),
              ]

