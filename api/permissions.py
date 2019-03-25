from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class HasGroupPermission(BasePermission):
    @staticmethod
    def _is_in_group(user, group_id):
        '''

        :param user:
        :param group_id:
        :return:
        '''
        try:
            return Group.objects.get(id=group_id).user_set.filter(
                id=user.id).exists()
        except Group.DoesNotExist:
            return False

    def has_permission(self, request, view):
        _required_groups = view.permission_groups.get(view.action)
        if request.user.is_superuser:
            return True
        elif _required_groups is None:
            return False
        else:
            return any(
                [self._is_in_group(request.user, group_id) for group_id in
                 _required_groups])
