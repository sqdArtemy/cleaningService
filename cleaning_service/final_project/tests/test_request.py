import pytest
import json
import factory
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import RequestFactory, RequestStatusFactory
from core.models import Request, RequestStatus
sys.path.append('..')
from api.view import RequestViewSet, RequestStatusViewSet

pytestmark = pytest.mark.django_db  # Links with django data base


@pytest.fixture  # Let us interact with DRF endpoints
def api_client():
    client = APIClient()
    # client.credentials(HTTP_AUTHORIZATION='Bearer ' + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNzQwOTY0LCJpYXQiOjE2NTM3NDA2NjQsImp0aSI6ImUwOGI1NWIzYzk5YTQ5NTNiZjFlNmZjNjgwMzRlMmMxIiwidXNlcl9pZCI6Mn0.m1k2OJ8a559LUFyzem-qmEilQIn0lY7B9n4fYhqvJUQ")
    return client


# Tests for user roles
class TestRequestStatus:
    endpoint = '/request_statuses/'  # Needed endpoints
    RequestStatusViewSet.permission_classes = [permissions.AllowAny]

    def test_list(self, mocker, rf):  # <----------Tests list-view
        # Arrange
        url = self.endpoint
        request = rf.get(url)

        RequestStatusFactory.create_batch(3)  # Creating test objects

        view = RequestStatusViewSet.as_view({'get': 'list'})
        response = view(request).render()

        # Comparing results
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        # Arrange
        request_status = RequestStatusFactory()
        url = f'/request_status/{request_status.id}'
        request = rf.get(url)

        expected_json = {
            'status': request_status.status,
        }

        view = RequestStatusViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=request_status.id).render()

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json


# Tests for users
class TestRequest:
    endpoint = '/requests/'  # Needed endpoints
    RequestViewSet.permission_classes = [permissions.AllowAny]

    def test_list(self, api_client):  # <----------Tests list-view
        RequestFactory.create_batch(10)  # Creates 10 random users

        response = api_client.get(self.endpoint)

        # Comparing results
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        # Arrange
        my_request = RequestFactory()
        url = f'{self.endpoint[0:-2]}/{my_request.id}'
        request = rf.get(url)

        expected_json = {  # Data for comparison
            'status': my_request.status.status,
            'customer': my_request.customer.username,
            'service': my_request.service.name,
            'total_area': my_request.total_area,
            'total_cost': my_request.total_cost,
            'address': my_request.address,
        }

        view = RequestViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=my_request.id).render()

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        # Arrange
        my_request = RequestFactory()
        url = f'{self.endpoint[0:-2]}/{my_request.id}'

        response = api_client.delete(url)

        # Comparing results
        assert response.status_code == 204
        assert Request.objects.all().count() == 0

    def test_create(self, api_client):  # <----------Tests creating an instance functionality
        request = RequestFactory()

        expected_json = {
            'status': request.status.status,
            'customer': request.customer.username,
            'service': request.service.name,
            'total_area': request.total_area,
            'total_cost': request.total_cost,
            'address': request.address,
        }

        response = api_client.post(
            path=self.endpoint,
            data=expected_json,
            format='json'
        )

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, mocker, rf):   # <----------Tests updating an instance functionality
        old_request = RequestFactory()
        new_request = RequestFactory()
        request_dict = {
            'status': new_request.status.status,
            'customer': old_request.customer.username,
            'service': old_request.service.name,
            'total_area': new_request.total_area,
            'address': new_request.address,
        }

        url = f'{self.endpoint[0:-2]}/{old_request.id}'
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(request_dict)
        )

        # Mocking
        mocker.patch.object(RequestViewSet, 'get_object', return_value=old_request)
        mocker.patch.object(Request, 'save')

        view = RequestViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_request.id).render()

        # Deleting total cost because it depends on a service which is different in both cases
        json_response = json.loads(response.content)
        del json_response['total_cost']

        assert response.status_code == 200
        assert json_response == request_dict