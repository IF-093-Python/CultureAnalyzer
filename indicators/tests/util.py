from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

__all__ = ['USERNAME', 'PASSWORD', 'create_user_with_role']


USERNAME = 'test_user'
PASSWORD = 'test_password'


def create_user_with_role(role_name, permissions):
    """
    Create user with a given role and permissions
    :param role_name: string with a name of role
    :param permissions: dictionary where key is app_label and value is a list
    of code names
    """
    user = get_user_model().objects.create_user(username=USERNAME,
                                                password=PASSWORD)

    user_role = Group.objects.get(name=role_name)
    for app_label, codename_list in permissions.items():
        for codename in codename_list:
            user_role.permissions.add(
                    Permission.objects.get(
                                    content_type__app_label=app_label,
                                    codename=codename))
    user.groups.set([user_role])
