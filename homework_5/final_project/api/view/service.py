import sys
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins, viewsets
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

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):  # ViewSet
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        categories = Category.objects.all()
        return categories

    def create(self, request, *args, **kwargs):
        data = request.data

        new_category = Category.objects.create(naming=data["naming"])
        new_category.save()
        serializer = CategorySerializer(new_category)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data

        category = self.get_object(pk)
        category.naming = data['naming']
        category.save()

        serializer = CategorySerializer(category)
        return Response(serializer.data)


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

    class CategoryViewSet(viewsets.ModelViewSet):  # ViewSet
        serializer_class = CategorySerializer
        queryset = Category.objects.all()

        def get_queryset(self):
            categories = Category.objects.all()
            return categories

        def create(self, request, *args, **kwargs):
            data = request.data

            new_category = Category.objects.create(name=data["name"], cost=data['cost'], category=data['category'])
            new_category.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):  # ViewSet
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_queryset(self):
        services = Service.objects.all()
        return services

    def create(self, request, *args, **kwargs):
        data = request.data

        new_service = Service.objects.create(name=data["name"], cost=data["cost"], category=data["category"])
        new_service.save()
        serializer = ServiceSerializer(new_service)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data

        service = self.get_object(pk)
        service.name = data['name']
        service.cost = data['cost']
        service.category = data['category']
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

