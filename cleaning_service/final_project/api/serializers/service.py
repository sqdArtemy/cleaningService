from rest_framework import serializers
from core.models.service import Service, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['naming']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'cost', 'category')

    name = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_name(self, service):
        return service.name
    def get_cost(self, service):
        return service.cost
    def get_category(self, service):
        return service.category.naming