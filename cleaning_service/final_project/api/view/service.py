from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers.service import CategorySerializer, ServiceSerializer
from core.models.service import Service, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


# Views for category
class CategoryViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        categories = Category.objects.all()
        return categories

    def list(self, request: Category, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


# Views for service
class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ServiceSerializer

    def get_category(self, naming):  # Obtaining company object
        return Category.objects.filter(naming=naming).first()

    def get_queryset(self):
        services = Service.objects.select_related('category')
        return services

    def create(self, request, *args, **kwargs):
        data = request.data

        new_service = Service.objects.create(name=data["name"], cost=data["cost"],
                                             category=self.get_category(data['category']))
        new_service.save()
        serializer = ServiceSerializer(new_service)
        return Response(serializer.data)

    def list(self, request: Service, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        data = request.data
        service_object = Service.objects.all()
        service = get_object_or_404(service_object, pk=pk)

        service.name = data['name']
        service.cost = data['cost']
        service.category = self.get_category(data['category'])
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

