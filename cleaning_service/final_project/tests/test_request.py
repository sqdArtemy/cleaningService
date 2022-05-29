import pytest
import json
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import RequestFactory, RequestStatusFactory
from core.models import Request, RequestStatus, User, Service
sys.path.append('..')
from api.view import RequestViewSet, RequestStatusViewSet
from .default_tests import default_test_delete, default_test_list, default_test_retrieve

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

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=RequestStatusFactory,
                          endpoint=self.endpoint, viewset=RequestStatusViewSet)

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=RequestStatusFactory, endpoint='request_status',
                              viewset=RequestStatusViewSet)


# Tests for users
class TestRequest:
    endpoint = '/requests/'  # Needed endpoints
    RequestViewSet.permission_classes = [permissions.AllowAny]

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=RequestFactory, endpoint=self.endpoint, viewset=RequestViewSet)

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=RequestFactory, endpoint='request', viewset=RequestViewSet,
                              foreign_keys={'customer': User, 'status': RequestStatus, 'service': Service})

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/request', factory=RequestFactory(), model=Request)

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
