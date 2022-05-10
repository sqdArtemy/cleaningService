import sys
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.service import CategorySerializer, ServiceSerializer
sys.path.append(".")
from core.models.service import Service, Category


# Views for category
@api_view(['GET'])
def categories_list(request, format=None):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryCreate(generics.CreateAPIView):  # Generics views
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []


class CategoryDetails(mixins.RetrieveModelMixin,  # APIView with mixins
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request,*args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Views for service
@api_view(['GET'])
def services_list(request, format=None):  # Function based view
    if request.method == 'GET':
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServicesList(generics.ListCreateAPIView):  # Generics views
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = []


class ServiceDetails(APIView):  # APIView
    def get_service(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        service = self.get_service(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service = self.get_service(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        request = self.get_service(pk)
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

