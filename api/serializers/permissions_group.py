from django.contrib.auth.models import Group
from rest_framework import serializers

__all__ = ['PermissionGroupSerializer']


class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
