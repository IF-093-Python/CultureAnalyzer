from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from api.serializers import ProfileSerializer
from api.serializers import SignUpSerializer

__all__ = ['SignUpView', 'ProfileView']


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class ProfileView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        current_user = self.request.user
        return current_user
