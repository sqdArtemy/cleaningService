from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.serializers.request import RequestSerializer, RequestStatusSerializer
from api.signals import company_notifier_signal
from core.models.request import Request, RequestStatus, Service, User


def data_validator(data):
    if int(data['max_hour_price']) < 0:  # Checks hour price filter
        raise serializers.ValidationError("Hour price value should be positive!")
    if int(data['min_rating_needed']) > 5 and int(data['min_rating_needed']):  # Checks minimum required rating filter
        raise serializers.ValidationError("Rating should be in range from 0 to 5!")
    if int(data['total_area']) < 0:  # Checks total area value
        raise serializers.ValidationError("Area value should be positive!")


# Views for request status
class RequestStatusViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestStatusSerializer

    def get_queryset(self):
        request_statuses = RequestStatus.objects.all()
        return request_statuses


# Views for request
class RequestViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RequestSerializer

    @staticmethod
    def get_status(status):  # Obtaining request status object
        return RequestStatus.objects.get(status=status)

    @staticmethod
    def get_service(name):  # Obtaining service object
        return Service.objects.get(name=name)

    @staticmethod
    def get_user(username):  # Obtaining user object
        return User.objects.get(username=username)

    def get_queryset(self):
        requests = Request.objects.select_related('customer', 'service', 'status')
        return requests

    def create(self, request, *args, **kwargs):
        data = request.data
        data_validator(data)  # Validating data

        new_request = Request.objects.create(customer=self.get_user(data["customer"]), company=None,
                                             service=self.get_service(data['service']), country=data['country'],
                                             status=self.get_status(data['status']), city=data['city'],
                                             address_details=data['address_details'], total_area=data['total_area'],
                                             max_hour_price=data['max_hour_price'],
                                             min_rating_needed=data['min_rating_needed'])

        if 'no_signal' not in data:  # Sending signal if it is not test
            post_save.connect(receiver=company_notifier_signal, sender=Request)
        new_request.save()

        # Disconnecting signal to avoid repetitive emitting
        post_save.disconnect(receiver=company_notifier_signal, sender=Request)
        serializer = RequestSerializer(new_request)
        return Response(serializer.data)

    def update(self, request: Request, pk):
        data = request.data
        data_validator(data)  # Validating data

        request_object = Request.objects.all()
        request = get_object_or_404(request_object, pk=pk)

        # Updating values in customer instance
        request.customer = request.customer
        request.service = request.service
        request.status = self.get_status(data['status'])
        request.total_area = data['total_area']
        request.country = data['country']
        request.city = data['city']
        request.company = self.get_user(data['company'])
        request.address_details = data['address_details']
        request.min_rating_needed = data['min_rating_needed']
        request.max_hour_price = data['max_hour_price']
        request.save()

        serializer = RequestSerializer(request)
        return Response(serializer.data)
