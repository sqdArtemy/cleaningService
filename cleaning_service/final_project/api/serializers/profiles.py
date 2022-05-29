from rest_framework import serializers
from core.models.profiles import User, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone', 'role',)

    role = serializers.SerializerMethodField()

    def get_role(self, user):
        return user.role.role
