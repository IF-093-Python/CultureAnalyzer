from django.contrib.auth import get_user_model
from django_filters import FilterSet

from CultureAnalyzer.constants import ADMIN_ID


class UserFilter(FilterSet):
    class Meta:
        model = get_user_model()
        fields = ['username', 'is_active']


def admin_search(request):
    """Admin can see all users except other admins.
    If admin is superuser he can see all users (even admins) except himself
    """

    users_in_view = get_user_model().objects.exclude(is_superuser=True)

    if not request.user.is_superuser:
        users_in_view = users_in_view.exclude(groups__id=ADMIN_ID)

    filtered_users = UserFilter(request.GET, queryset=users_in_view)

    return filtered_users
