from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.serializers.service import ServiceSerializer
from core.models import User, UserRole, Service


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'role']


class CustomUserSerializer(serializers.ModelSerializer):
    # Setting fields which are going to be excluded for each role
    COMPANY_EXCLUDE_FIELDS = {}
    CUSTOMER_EXCLUDE_FIELDS = {'hour_cost', 'users_rated', 'rating', 'services'}

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'phone', 'role', 'country', 'city', 'address_details', 'services',
                  'rating', 'picture', 'hour_cost', 'users_rated', 'password')

    password = serializers.CharField(write_only=True)
    role = serializers.CharField(source='role.role')
    services = ServiceSerializer(read_only=True, many=True)  # Many to many field

    # Overloading initializer in order to hide some field of company when we display customer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(args) is not 0:
            arg = args[0]
            if isinstance(arg, User):  # If we ask for 1 object, not queryset
                # Decide which role user has and which field we are going to exclude
                exclude = self.CUSTOMER_EXCLUDE_FIELDS if arg.role.role == "Customer" else self.COMPANY_EXCLUDE_FIELDS

                existing = set(self.fields)  # Get all fields
                # Exclude particular fields which we are not going to see
                for field_name in existing.intersection(exclude):
                    self.fields.pop(field_name)

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
        # Getting data
        role_data = data.pop('role').get('role')
        role = UserRole.objects.filter(role=role_data).first()
        picture = data.pop('picture')

        new_user = User.objects.create_user(role=role, **data)

        if len(services) != 0:  # If user have services -> process and add it to the User object
            if len(services[0]) != 0:
                self.services_setter(services, new_user)

        new_user.picture=picture
        new_user.save()
        return new_user

    def update(self, data: dict, services: list[str], pk):
        # Getting data
        role_data = data.pop('role').get('role')
        picture = data.pop('picture')
        role = UserRole.objects.filter(role=role_data).first()
        user = self.instance

        # Setting new data
        password = data.pop('password')
        for key, value in data.items():
            setattr(user, key, value)
        user.role = role
        user.set_password(password)
        user.picture = picture

        if len(services) != 0:  # If user have services -> process and add it to the User object
            if len(services[0]) != 0:
                self.services_setter(services, user)

        user.save()
        return user
