from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from api.permissions import IsAdmin, IsMentor, IsSuperAdmin
from api.permissions import is_mentor, is_admin, is_superadmin
from api.service import get_superadmin_users, get_mentor_users, get_admin_users
from .serializers import UserSerializer
from feedbacks.models import Feedback, Recommendation
from feedbacks.serializers import FeedbackSerializer, RecommendationSerializer
from indicators.models import CountryIndicator
from indicators.serializers import CountryIndicatorSerializer
from users.models import CustomUser


@api_view(['GET'])
def protected_view(request):
    return Response({'username': f'{request.user.username}'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperAdmin | IsAdmin | IsMentor,)
    queryset = CustomUser.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return self.query_by_role(user)

    def query_by_role(self, user):
        queryset = super(UserViewSet, self).get_queryset()
        if is_superadmin(user):
            queryset = get_superadmin_users()
        elif is_admin(user):
            queryset = get_admin_users()
        elif is_mentor(user):
            queryset = get_mentor_users()
        return queryset


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_fields = ('indicator', )
    search_fields = ('feedback', )


class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class RecommendationList(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    search_fields = ('recommendation', )


class RecommendationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer


class CountryIndicatorList(generics.ListCreateAPIView):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer


class CountryIndicatorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CountryIndicator.objects.all()
    serializer_class = CountryIndicatorSerializer
