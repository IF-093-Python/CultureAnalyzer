from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view()),
        path('refresh/', TokenRefreshView.as_view()),
    ])),
]
