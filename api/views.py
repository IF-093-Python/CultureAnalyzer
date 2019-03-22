from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsAdmin, CanChangeUser
from api.serializers import (SignUpSerializer, FeedbackSerializer,
                             ProfileSerializer, BlockProfileSerializer,
                             AdminListSerializer)
from feedbacks.models import Feedback
from users.filters import admin_search

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet', 'BlockProfileView',
           'AdminListView']


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class ProfileView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class AdminListView(generics.ListAPIView):
    model = get_user_model()
    serializer_class = AdminListSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        return admin_search(self.request).qs


class BlockProfileView(generics.RetrieveUpdateAPIView):
    model = get_user_model()
    serializer_class = BlockProfileSerializer
    permission_classes = (IsAdmin, CanChangeUser)

    def get_queryset(self):
        return get_user_model().objects.all()
