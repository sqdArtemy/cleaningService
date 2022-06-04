from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers.request import RequestStatusSerializer, RequestSerializer
from core.models.request import Request, RequestStatus, Service, User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from api.signals import company_notifier_signal
from django.db.models.signals import post_save

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

    def get_status(self, status):  # Obtaining request status object
        return RequestStatus.objects.get(status=status)

    def get_service(self, name):  # Obtaining service object
        return Service.objects.get(name=name)

    def get_user(self, username):  # Obtaining user object
        return User.objects.get(username=username)

    def get_queryset(self):
        requests = Request.objects.select_related('customer', 'service', 'status')
        return requests

    def create(self, request, *args, **kwargs):
        data = request.data

        new_request = Request.objects.create(customer=self.get_user(data["customer"]), total_area=data['total_area'],
                                             service=self.get_service(data['service']), country=data['country'],
                                             status=self.get_status(data['status']), city=data['city'],
                                             address_details=data['address_details'], company=None)
        if 'no_signal' not in data: post_save.connect(receiver=company_notifier_signal, sender=Request)
        new_request.save()
        serializer = RequestSerializer(new_request)
        return Response(serializer.data)


    def update(self, request, pk):
        data = request.data
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
        request.save()

        serializer = RequestSerializer(request)
        return Response(serializer.data)
