from rest_framework import serializers

from users.models import CustomUser

__all__ = ['SuperuserSerializer', 'AdminUserSerializer',
           'MentorUserSerializer', 'TraineeUserSerializer']


class SuperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('id',)


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'is_staff', 'is_active',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class MentorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name', 'is_staff')
        read_only_fields = ('id', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TraineeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
