from django.urls import path

from .views import CountryIndicatorListView, CountryIndicatorCreate, \
    CountryIndicatorUpdate, CountryIndicatorDelete


app_name = 'country_indicator'


urlpatterns = [
    path('', CountryIndicatorListView.as_view(),
         name='country_indicator_list'),
    path('create/', CountryIndicatorCreate.as_view(),
         name='country_indicator_create'),
    path('<int:pk>/update/', CountryIndicatorUpdate.as_view(),
         name='country_indicator_update'),
    path('<int:pk>/delete/', CountryIndicatorDelete.as_view(),
         name='country_indicator_delete'),
]
