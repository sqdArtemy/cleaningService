import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from api.serializers import CustomUserSerializer, UserRoleSerializer
from core.models.profiles import User, UserRole, Service
from django.shortcuts import get_object_or_404


# Views for user role
class UserRoleViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoleSerializer

    def get_queryset(self):
        user_roles = UserRole.objects.all()
        return user_roles


# Views for user
class UserViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer

    def get_role(self, name):  # Obtaining user role object
        return UserRole.objects.filter(role=name).first()

    def get_queryset(self):
        users = User.objects.select_related('role')
        users = User.objects.prefetch_related('services')
        return users

    def services_setter(self, data, obj):  # Function which properly sets many-to-many services
        service_list = []
        for service in data['services']:  # Getting names of services
            service_obj = Service.objects.get(name=service)
            service_list.append(service_obj)

        obj.services.add(*service_list)  # Adding service objects to user
        obj.save()

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data

        new_user = User.objects.create_user(name=data['name'], email=data['email'], phone=data['phone'],
                                            role=self.get_role(data['role']), country=data['country'],
                                            city=data['city'], address_details=data['address_details'],
                                            username=data['username'], password=data['password'])
        new_user.save()

        if 'services' in data:  # If user have services -> process and add it to the User object
            self.services_setter(data, new_user)

        serializer = CustomUserSerializer(new_user)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        user_object = self.get_queryset()
        user = get_object_or_404(user_object, pk=pk)
        user.username = data['username']
        user.name = data['name']
        user.email = user.email
        user.country = data['country']
        user.city = data['city']
        user.address_details = data['address_details']
        user.phone = data['phone']
        user.role = user.role
        user.set_password(user.password)
        user.save()

        if 'services' in data:  # If user have services -> process and add it to the User object
            self.services_setter(data, user)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)