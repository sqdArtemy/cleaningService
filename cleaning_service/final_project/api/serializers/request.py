from rest_framework import serializers
from core.models.request import Request, RequestStatus


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['status']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['service', 'customer', 'status', 'total_area', 'address']

    status = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()

    def get_status(self, request):
        return request.status.status
    def get_customer(self, request):
        return request.customer.name
    def get_service(self, request):
        return request.service.name

