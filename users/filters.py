import django_filters

from django.contrib.auth.models import User

from CultureAnalyzer.constants import SUPER_USER_ID


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'is_active']


def admin_search(request):
    """Only admin can change role and block another user
    and only superadmin can change role and block another admins
    except itself
    """
    result = User.objects.exclude(profile__role__name='Admin')

    if request.user.id == SUPER_USER_ID:
        result = User.objects.exclude(pk=request.user.id)

    result_filter = UserFilter(request.GET, queryset=result)

    return result_filter
