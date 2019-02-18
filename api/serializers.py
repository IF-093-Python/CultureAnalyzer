from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source='profile.id')
    role = serializers.CharField(source='profile.role.name')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'email', 'first_name', 'last_name',
            'is_active', 'profile_id', 'role')
        read_only_fields = ('id',)
