from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, decorators, mixins, status
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response

from api.serializers import CustomUserSerializer, UserRoleSerializer
from core.models.profiles import Service, User, UserRole
from core.utility.filters import UserFilter


# Views for user role
class UserRoleViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoleSerializer

    def get_queryset(self):
        user_roles = UserRole.objects.all()
        return user_roles


# Views for user
class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                  viewsets.GenericViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    @staticmethod
    def get_role(role):  # Obtaining user role object
        return UserRole.objects.filter(role=role).first()

    def get_queryset(self):
        users = User.objects.select_related('role').prefetch_related('services__category')
        return users

    @staticmethod
    def services_setter(services: list[str], obj):  # Function which properly sets many-to-many services
        service_list = []
        for service in services:  # Getting names of services
            service_obj = Service.objects.get(name=service)
            service_list.append(service_obj)

        obj.services.add(*service_list)  # Adding service objects to user
        obj.save()

    def update(self, request, pk, *args, **kwargs):
        _mutable = request.data._mutable  # Current mutability state
        request.data._mutable = True  # Set mutability to True
        services = request.data.pop('services')  # Removing services here, because they will be added separately
        request.data._mutable = _mutable  # Changing to original state

        user = self.get_object()
        serializer = CustomUserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(serializer.validated_data, services, pk)
        serializer = CustomUserSerializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Separate declaration of create method is needed to create new user without authorization,
# because obviously new user don`t have an account
@decorators.api_view(['POST'])
@decorators.authentication_classes([])
@decorators.permission_classes([AllowAny])
def create(request, *args, **kwargs):
    services = request.data.pop('services')

    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.create(serializer.validated_data, services)
    serializer = CustomUserSerializer(instance=user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
