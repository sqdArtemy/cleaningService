from rest_framework import serializers
import sys
sys.path.append("...")
from core.models.profiles import User, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'role']
    role = serializers.SerializerMethodField()
    def get_role(self, user):
        return user.role.role