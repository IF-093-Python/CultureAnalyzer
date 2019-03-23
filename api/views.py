from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets


from api.serializers import SignUpSerializer, FeedbackSerializer, \
    ProfileSerializer
from api.permissions import HasGroupPermission
from feedbacks.models import Feedback

__all__ = ['SignUpView', 'ProfileView', 'FeedbackViewSet']


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

    permission_classes = [HasGroupPermission]
    permission_groups = {
        'list': ['Trainee'],
        'create': ['Mentor'],
        'partial_update': ['Mentor'],
        'retrieve': ['Mentor'],
        'destroy': ['Mentor'],
        }
