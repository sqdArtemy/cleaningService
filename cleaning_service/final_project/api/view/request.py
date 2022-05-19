from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers.request import RequestStatusSerializer, RequestSerializer
from core.models.request import Request, RequestStatus, Service, User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


# Views for request status
class RequestStatusViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RequestStatusSerializer
    queryset = RequestStatus.objects.all()

    def get_queryset(self):
        request_statuses = Request.objects.all()
        return request_statuses

    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


# Views for request
class RequestViewSet(viewsets.ModelViewSet):  # ViewSet
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get_status(self, name):  # Obtaining request status object
        return RequestStatus.objects.filter(role=name).first()

    def get_service(self, name):  # Obtaining service object
        return Service.object.filter(name=name).first()

    def get_user(self, email):  # Obtaining user object
        return User.object.filter(email=email).first()

    def get_queryset(self):
        requests = Request.objects.all()
        return requests

    def create(self, request, *args, **kwargs):
        data = request.data

        new_request = Request.objects.create(customer=self.get_user(data["customer"]), service=self.get_service(data['service']),
                                           status=self.get_status(data['status']), total_area=data['total_area'],
                                        address=data['address'],total_cost=data['total_cost'])
        new_request.save()
        serializer = RequestSerializer(new_request)
        return Response(serializer.data)

    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data
        request_object = Request.objects.all()
        request = get_object_or_404(request_object, pk=pk)

        request.customer = self.get_user(data["customer"])
        request.service = self.get_service(data['service'])
        request.status = self.get_status(data['status'])
        request.total_area = data['total_area']
        request.total_cost = data['total_cost']
        request.address = data['address']
        request.save()

        serializer = RequestSerializer(request)
        return Response(serializer.data)

