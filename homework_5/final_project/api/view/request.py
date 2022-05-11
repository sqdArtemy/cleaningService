import sys
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins, viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.request import RequestStatusSerializer, RequestSerializer
sys.path.append(".")
from core.models.request import Request, RequestStatus


# Views for request status
@api_view(['GET'])
def request_statuses_list(request, format=None):
    if request.method == 'GET':
        request_statuses = RequestStatus.objects.all()
        serializer = RequestStatusSerializer(request_statuses, many=True)
        return Response(serializer.data)


class RequestStatusesList(generics.ListAPIView):  # Generics views
    queryset = RequestStatus.objects.all()
    serializer_class = RequestStatusSerializer
    permission_classes = []


class RequestStatusDetails(mixins.RetrieveModelMixin,  # APIView with mixins
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = RequestStatus.objects.all()
    serializer_class = RequestStatusSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request,*args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Views for request
@api_view(['GET'])
def requests_list(request, format=None):  # Function based view
    if request.method == 'GET':
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)


class RequestsList(generics.ListCreateAPIView):  # Generics views
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = []


class RequestDetails(APIView):  # APIView
    def get_request(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        request = self.get_request(pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        request = self.get_request(pk)
        serializer = RequestSerializer(request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        request = self.get_request(pk)
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestViewSet(viewsets.ModelViewSet):  # ViewSet
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get_queryset(self):
        requests = Request.objects.all()
        return requests

    def create(self, request, *args, **kwargs):
        data = request.data

        new_request = Request.objects.create(customer=data["customer"], service=data['service'],
                                           status=data['status'], total_area=data['total_area'],
                                        address=data['address'],total_cost=data['total_cost'])
        new_request.save()
        serializer = RequestSerializer(new_request)
        return Response(serializer.data)

    def update(self, request, pk):
        data = request.data

        request = self.get_object(pk)
        request.customer = data["customer"]
        request.service = data['service']
        request.status = data['status']
        request.total_area = data['total_area']
        request.total_cost = data['total_cost']
        request.address = data['address']
        request.save()

        serializer = RequestSerializer(request)
        return Response(serializer.data)

