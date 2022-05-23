from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from api.serializers import UserSerializer, UserRoleSerializer
from core.models.profiles import User, UserRole
from django.shortcuts import get_object_or_404


# Views for user role
class UserRoleViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticated)
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()

    def get_queryset(self):
        user_roles = UserRole.objects.all()
        return user_roles

    def list(self, request: User, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


# Views for user
class UserViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_role(self, name):  # Obtaining user role object
        return UserRole.objects.filter(role=name).first()

    def get_queryset(self):
        users = User.objects.all()
        return users

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data

        new_user = User.objects.create(name=data['name'], email=data['email'],
                                       phone=data['phone'], role=self.get_role(['role']))
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data)

    def list(self, request: User, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        user_object = User.objects.all()
        user = get_object_or_404(user_object, pk=pk)
        user.name = data['name']
        user.email = user.email
        user.phone = data['phone']
        user.role = self.get_role(data['role'])
        user.password = user.password
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)