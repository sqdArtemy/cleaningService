from rest_framework import serializers
from core.models.service import Service, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['naming']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'cost', 'category', 'company']

    company = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, service):
        return service.category.naming
    def get_company(self, service):
        return service.company.username
