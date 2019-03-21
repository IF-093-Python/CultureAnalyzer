from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import SignUpView, FeedbackViewSet, ProfileView

__all__ = ['urlpatterns']

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet, basename='api_feedback')

urlpatterns = [
    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view()),
        path('refresh/', TokenRefreshView.as_view()),
    ])),
    path('sign-up/', SignUpView.as_view()),
    path('profile/', ProfileView.as_view()),
]

urlpatterns += router.urls
