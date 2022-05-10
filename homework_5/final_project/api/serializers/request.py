from rest_framework import serializers
import sys
sys.path.append("...")
from core.models.request import Request, RequestStatus


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['id', 'status']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'service', 'customer', 'status', 'total_area', 'address', 'total_cost']
