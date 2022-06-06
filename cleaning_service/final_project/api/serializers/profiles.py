from rest_framework import serializers

from api.serializers.service import ServiceSerializer
from core.models import User, UserRole, Service


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone', 'role', 'country', 'city', 'address_details', 'services',
                  'rating', 'profile_pic', 'hour_cost', 'users_rated', 'password')

    password = serializers.CharField(write_only=True)
    role = serializers.CharField(source='role.role')
    services = ServiceSerializer(read_only=True, many=True)  # Many to many field

    @staticmethod
    def services_setter(services: list[str], obj):  # Function which properly sets many-to-many services
        service_list = []
        for service in services:  # Getting names of services
            service_obj = Service.objects.get(name=service)
            service_list.append(service_obj)

        obj.services.add(*service_list)  # Adding service objects to user
        obj.save()

    # Overloading create func in order to set up password correctly and if extra args are passed -> they ignored
    def create(self, data: dict, services: list[str]):
        role_data = data.pop('role').get('role')
        role = UserRole.objects.filter(role=role_data).first()

        new_user = User.objects.create_user(role=role, **data)

        if services is not None:  # If user have services -> process and add it to the User object
            self.services_setter(services, new_user)

        new_user.save()
        return new_user

    def update(self, instance: User, validated_data: dict):
        pass
