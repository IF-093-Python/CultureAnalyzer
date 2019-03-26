from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

__all__ = ['create_user_with_role']


def create_user_with_role(role_id, permission=None, username='Username',
                          password='pass', email='u@s.er'):
    """
    Create user in db with a given role and permissions
    """
    if get_user_model().objects.filter(username=username).exists():
        return None
    user = get_user_model().objects.create_user(username=username, email=email,
                                                password=password)
    role = Group.objects.get(pk=role_id)
    if permission:
        role.permissions.add(
            Permission.objects.get(content_type__app_label='groups',
                                   codename=permission))
    user.groups.set([role])
    return user
