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
        fields = ('name', 'email', 'phone', 'role')
    role = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    def get_role(self, user):
        return user.role.role
    def get_name(self, user):
        return user.name
    def get_email(self, user):
        return user.email
    def get_phone(self, user):
        return user.phone