from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins, viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
import sys
from ..serializers.profiles import UserSerializer, UserRoleSerializer
sys.path.append(".")
from core.models.profiles import User, UserRole


# Views for user role
@api_view(['GET'])
def user_roles_list(request, format=None):
    if request.method == 'GET':
        user_roles = UserRole.objects.all()
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response(serializer.data)


class UserRolesList(generics.ListAPIView):  # Generics views
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = []


class UserRoleDetails(mixins.RetrieveModelMixin,  # APIView with mixins
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request,*args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Views for user
@api_view(['GET'])
def users_list(request, format=None):  # Function based view
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UsersList(generics.ListCreateAPIView):  # Generics views
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class UserDetails(APIView):  # APIView
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):  # ViewSet
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        categories = User.objects.all()
        return categories

    def create(self, request, *args, **kwargs):
        data = request.data

        new_user = User.objects.create(name=data["name"], email=data['email'],
                                           phone=data['phone'], role=data['role'])
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data

        user = self.get_object(pk)
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.role = data['role']
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)