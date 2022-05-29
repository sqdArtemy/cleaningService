import pytest
import json
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import ServiceFactory, CategoryFactory
from core.models import Service, Category, User
sys.path.append('..')
from api.view import ServiceViewSet, CategoryViewSet
from .default_tests import default_test_list, default_test_delete, default_test_retrieve

pytestmark = pytest.mark.django_db  # Links with django data base


@pytest.fixture  # Let us interact with DRF endpoints
def api_client():
    client = APIClient()
    # client.credentials(HTTP_AUTHORIZATION='Bearer ' + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNzQwOTY0LCJpYXQiOjE2NTM3NDA2NjQsImp0aSI6ImUwOGI1NWIzYzk5YTQ5NTNiZjFlNmZjNjgwMzRlMmMxIiwidXNlcl9pZCI6Mn0.m1k2OJ8a559LUFyzem-qmEilQIn0lY7B9n4fYhqvJUQ")
    return client


# Tests for user roles
class TestCategory:
    CategoryViewSet.permission_classes = (permissions.AllowAny,)
    endpoint = '/categories/'  # Needed endpoints

    def test_list(self, mocker, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=CategoryFactory, endpoint=self.endpoint, viewset=CategoryViewSet)

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, viewset=CategoryViewSet, endpoint='category', factory=CategoryFactory)


# Tests for users
class TestService:
    ServiceViewSet.permission_classes = (permissions.AllowAny,)
    endpoint = '/services/'  # Needed endpoints

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=ServiceFactory, endpoint=self.endpoint, viewset=ServiceViewSet)

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=ServiceFactory, endpoint='service',
                              viewset=ServiceViewSet, foreign_keys={'category': Category, 'company': User})

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/service', factory=ServiceFactory(), model=Service)

    def test_create(self, api_client):  # <----------Tests creating an instance functionality
        service = ServiceFactory()

        expected_json = {
            'name': service.name,
            'cost': service.cost,
            'category': service.category.naming,
            'company': service.company.username,
        }

        response = api_client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, mocker, rf):   # <----------Tests updating an instance functionality
        old_service = ServiceFactory()
        new_service = ServiceFactory()
        service_dict = {
            'name': new_service.name,
            'cost': new_service.cost,
            'category': new_service.category.naming,
            'company': old_service.company.username,
        }

        url = f'{self.endpoint[0:-2]}/{old_service.id}'
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(service_dict)
        )

        # Mocking
        mocker.patch.object(ServiceViewSet, 'get_object', return_value=old_service)
        mocker.patch.object(Service, 'save')

        view = ServiceViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_service.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == service_dict