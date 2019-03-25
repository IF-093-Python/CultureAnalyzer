from django.contrib.auth import get_user_model
from rest_framework import serializers

__all__ = ['BlockProfileSerializer', 'AdminListSerializer']


class BlockProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'is_active', 'groups')


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'is_active', 'groups')
