from django.contrib.auth import get_user_model
from django_filters import FilterSet


class UserFilter(FilterSet):
    class Meta:
        model = get_user_model()
        fields = ['username', 'is_active']


def admin_search(request):
    pass
