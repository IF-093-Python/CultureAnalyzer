from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class HasGroupPermission(BasePermission):
    @staticmethod
    def is_in_group(user, role_id):
        '''
        check if the allowed role corresponds to the user role
        :return: bool, is group with group_id contains user
        '''
        try:
            return Group.objects.get(id=role_id).user_set.filter(
                id=user.id).exists()
        except Group.DoesNotExist:
            return False

    def has_permission(self, request, view):
        required_groups = view.permission_groups.get(view.action)
        if request.user.is_superuser:
            return True
        elif required_groups is None:
            return False
        return any(
            [self.is_in_group(request.user, role_id) for role_id in
             required_groups])
