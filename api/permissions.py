from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class HasGroupPermission(BasePermission):
    @staticmethod
    def is_in_group(user, group_id):
        '''
        Сhecking which group is the user
        :return: bool, is group with group_id contains user
        '''
        try:
            return Group.objects.get(id=group_id).user_set.filter(
                id=user.id).exists()
        except Group.DoesNotExist:
            return False

    def has_permission(self, request, view):
        required_groups = view.permission_groups.get(view.action)
        if request.user.is_superuser:
            return True
        elif required_groups is None:
            return False
        else:
            return any(
                [self.is_in_group(request.user, group_id) for group_id in
                 required_groups])
