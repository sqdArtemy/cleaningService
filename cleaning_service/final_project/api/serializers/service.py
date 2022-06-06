from rest_framework import serializers

from core.models.service import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('naming',)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'hours_required', 'category', 'picture', 'description')

    category = serializers.CharField(source='category.naming')

    @staticmethod
    def get_category(service):
        return service.category.naming
