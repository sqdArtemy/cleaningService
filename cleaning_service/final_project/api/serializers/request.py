from rest_framework import serializers

from core.models.request import Request, RequestStatus


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['id', 'status']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'service', 'customer', 'status', 'total_area', 'total_cost', 'address_details', 'country', 'city',
                  'company', 'min_rating_needed', 'max_hour_price')

    status = serializers.CharField(source='status.status')
    customer = serializers.CharField(source='customer.username')
    service = serializers.CharField(source='service.name')
    company = serializers.SerializerMethodField()

    @staticmethod
    def get_status(request):
        return request.status.status

    @staticmethod
    def get_customer(request):
        return request.customer.username

    @staticmethod
    def get_service(request):
        return request.service.name

    @staticmethod
    def get_company(request):
        try:
            return request.company.username
        except AttributeError:
            return None
