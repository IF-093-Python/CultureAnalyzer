from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.permissions import IsAdmin, IsMentor, IsSuperAdmin
from api.permissions import is_mentor, is_admin, is_superadmin
from api.service import get_superadmin_users, get_mentor_users, get_admin_users
from .serializers import UserSerializer


@api_view(['GET'])
def protected_view(request):
    return Response({'username': f'{request.user.username}'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperAdmin | IsAdmin | IsMentor,)
    queryset = User.objects.none()
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
