from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from api.serializers import CustomUserSerializer, UserRoleSerializer
from core.models.profiles import User, UserRole
from django.shortcuts import get_object_or_404


# Views for user role
class UserRoleViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoleSerializer

    def get_queryset(self):
        user_roles = UserRole.objects.all()
        return user_roles

    def list(self, request: User, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


# Views for user
class UserViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer

    def get_role(self, name):  # Obtaining user role object
        return UserRole.objects.filter(role=name).first()

    def get_queryset(self):
        users = User.objects.select_related('role')
        return users

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data

        new_user = User.objects.create_user(name=data['name'], email=data['email'],
                                            phone=data['phone'], role=self.get_role(data['role']),
                                            username=data['username'], password=data['password'])
        new_user.save()
        serializer = CustomUserSerializer(new_user)
        return Response(serializer.data)

    def list(self, request: User, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        user_object = self.get_queryset()
        user = get_object_or_404(user_object, pk=pk)
        user.username = data['username']
        user.name = data['name']
        user.email = user.email
        user.phone = data['phone']
        user.role = user.role
        user.set_password(user.password)
        user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)