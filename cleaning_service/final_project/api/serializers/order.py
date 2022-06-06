from rest_framework import serializers

from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('notification', 'company', 'total_cost', 'request', 'accepted')

    company = serializers.CharField(source='notification.user.username')

    @staticmethod
    def get_company(order):
        return order.notification.user.username
