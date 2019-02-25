from django_filters import FilterSet

from CultureAnalyzer.constants import SUPER_USER_ID
from .models import CustomUser

__all__ = ['admin_search']


class UserFilter(FilterSet):
    class Meta:
        model = CustomUser
        fields = ['username', 'is_active']


def admin_search(request):
    """Admin can see all users except other admins
    if admin is superuser he can see all users (even admins) except himself
    """

    users_in_view = CustomUser.objects.exclude(is_superuser=True)

    if request.user.id == SUPER_USER_ID:
        users_in_view = CustomUser.objects.exclude(pk=request.user.id)

    filtered_users = UserFilter(request.GET, queryset=users_in_view)

    return filtered_users
