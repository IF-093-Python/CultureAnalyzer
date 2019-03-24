from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

__all__ = ['USERNAME', 'PASSWORD', 'create_user_with_role']


USERNAME = 'test_user'
PASSWORD = 'test_password'


def create_user_with_role(role_id, permissions):
    """
    Create user in db with a given role and permissions

    :param role_id: role id
    :param permissions: tuple with code names
    """
    user = get_user_model().objects.create_user(username=USERNAME,
                                                password=PASSWORD)

    user_role = Group.objects.get(pk=role_id)
    for codename in permissions:
        user_role.permissions.add(Permission.objects.get(codename=codename))
    user.groups.set([user_role])
