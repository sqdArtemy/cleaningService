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
        data: dict = request.data
        services = data.pop('services', None)
        # TODO: try using >>> user = self.get_object()
        user_object = self.get_queryset()
        user = get_object_or_404(user_object, pk=pk)

        # for key, value in data.items():
        #     setattr(user, key, value)

        user.username = data['username']
        user.name = data['name']
        user.country = data['country']
        user.city = data['city']
        user.address_details = data['address_details']
        user.phone = data['phone']
        user.rating = data['rating']
        user.profile_pic = data['profile_pic']
        user.hour_cost = data['hour_cost']
        user.set_password(data.get('password'))

        user.save()

        if services is not None:  # If user have services -> process and add it to the User object
            self.services_setter(services, user)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


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
