from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


def is_in_group(user, group_id):
    try:
        print(Group.objects.get(id=group_id).user_set.filter(
            id=user.id))
        return Group.objects.get(id=group_id).user_set.filter(
            id=user.id).exists()
    except Group.DoesNotExist:
        return False


class HasGroupPermission(BasePermission):
    def has_permission(self, request, view):
        required_groups = view.permission_groups.get(view.action)
        if required_groups is None:
            return False
        elif '_Public' in required_groups:
            return True
        else:
            return any([is_in_group(request.user, group_id) for group_id in
                        required_groups])
