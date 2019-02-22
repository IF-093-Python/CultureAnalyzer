from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from api.views import (
    SignUpView,
    ProfileView
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view()),
        path('refresh/', TokenRefreshView.as_view()),
    ])),

    path('sign-up/', SignUpView.as_view()),
    path('profile/', ProfileView.as_view()),

    path('admin/', include([
        path('users/', NotImplementedError),
        path('users/<int:pk>', NotImplementedError),
    ])),
]

"""
/api/sign-up/           =>          log:pass
/api/profile/           =>          first_name:last_name
/api/admin/users        =>          username:role(read)
/api/admin/users/{id}   =>          username:role(patch)
"""
