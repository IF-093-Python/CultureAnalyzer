from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import *
from api.serializers.users import *
from api.service import *
from api.utils import first_hit_value
from users.models.custom_user import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.none()

    def get_permissions(self):
        user = self.request.user
        permissions = (IsSuperAdmin, IsAdmin, IsMentor, IsTrainee)
        self.permission_classes = [get_by_role(user=user,
                                               return_values=permissions,
                                               default=IsAuthenticated)]
        return super(UserViewSet, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        service = UserService(user)
        return service.get_queryset_by_role()

    def get_serializer_class(self):
        user_serializers = (SuperuserSerializer, AdminUserSerializer,
                            MentorUserSerializer, TraineeUserSerializer)
        return get_by_role(user=self.request.user,
                           return_values=user_serializers)


def get_by_role(user: CustomUser, return_values, default=None):
    return first_hit_value(conditions=(is_superadmin(user), is_admin(user),
                                       is_mentor(user), is_trainee(user)),
                           return_values=return_values,
                           default=default)
