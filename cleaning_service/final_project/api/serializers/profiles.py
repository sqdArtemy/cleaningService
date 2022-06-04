from rest_framework import serializers
from core.models.profiles import User, UserRole
from api.serializers.service import ServiceSerializer


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone', 'role', 'country', 'city', 'address_details', 'services',
                  'rating', 'profile_pic')

    role = serializers.SerializerMethodField()
    services = ServiceSerializer(read_only=True, many=True)  # Many to many field

    def get_role(self, user):
        return user.role.role
