from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import OrderSerializer
from core.models import Notification, Order
from core.utility.filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        orders = Order.objects.select_related('request', 'company', 'notification')
        return orders

    @staticmethod
    def get_notification(id_):
        return Notification.objects.get(id=id_)

    def create(self, request, *args, **kwargs):
        data = request.data

        order = Order.objects.create(notification=self.get_notification(data['notification']),
                                     accepted=data['accepted'])
        order.save()
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        data = request.data
        order.accepted = data['accepted']
        order.save()
        serializer = self.serializer_class(order, partial=True)
        return Response(serializer.data)
