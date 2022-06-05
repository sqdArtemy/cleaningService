from rest_framework import serializers

from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['notification', 'company', 'total_cost', 'request', 'accepted']

    notification = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_notification(self, order):
        return order.notification.id
    def get_request(self, order):
        return order.request.id
    def get_company(self, order):
        return order.notification.user.username



