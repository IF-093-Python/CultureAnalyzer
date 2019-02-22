from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers.sign_up import *
from users.models.custom_user import CustomUser


class SignUpView(generics.CreateAPIView):
    model = CustomUser
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    model = CustomUser
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        return CustomUser.objects.get(id=user.id)
