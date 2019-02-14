from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from api.views import (FeedbackList, FeedbackDetail, RecommendationList,
                       RecommendationDetail, CountryIndicatorDetail,
                       CountryIndicatorList)

from api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view()),
        path('refresh/', TokenRefreshView.as_view()),
    ])),
    path('feedbacks', FeedbackList.as_view()),
    path('feedbacks/<int:pk>', FeedbackDetail.as_view()),
    path('recommendations', RecommendationList.as_view()),
    path('recommendations/<int:pk>', RecommendationDetail.as_view()),
    path('indicators', CountryIndicatorList.as_view()),
    path('indicators/<int:pk>', CountryIndicatorDetail),
    path('protected/', protected_view),
]
