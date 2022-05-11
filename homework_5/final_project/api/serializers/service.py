from rest_framework import serializers
import sys
sys.path.append("...")
from core.models.service import Service, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['naming']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'cost', 'category']
