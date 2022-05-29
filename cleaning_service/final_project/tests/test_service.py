import pytest
import json
import factory
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import ServiceFactory, CategoryFactory
from core.models import Service, Category
sys.path.append('..')
from api.view import ServiceViewSet, CategoryViewSet

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
        # Arrange
        url = self.endpoint
        request = rf.get(url)

        CategoryFactory.create_batch(5)  # Creating test objects

        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request).render()

        # Comparing results
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        # Arrange
        category = CategoryFactory()
        url = f'/category/{category.id}'
        request = rf.get(url)

        expected_json = {
            'naming': category.naming,
        }

        view = CategoryViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=category.id).render()

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json


# Tests for users
class TestService:
    ServiceViewSet.permission_classes = (permissions.AllowAny,)
    endpoint = '/services/'  # Needed endpoints

    def test_list(self, api_client):  # <----------Tests list-view
        ServiceFactory.create_batch(10)  # Creates 10 random users

        response = api_client.get(self.endpoint)

        # Comparing results
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        # Arrange
        service = ServiceFactory()
        url = f'{self.endpoint[0:-2]}/{service.id}'
        request = rf.get(url)

        expected_json = {  # Data for comparison
            'name': service.name,
            'cost': service.cost,
            'category': service.category.naming,
            'company': service.company.username,
        }

        view = ServiceViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=service.id).render()

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        # Arrange
        service = ServiceFactory()
        url = f'{self.endpoint[0:-2]}/{service.id}'

        response = api_client.delete(url)

        # Comparing results
        assert response.status_code == 204
        assert Service.objects.all().count() == 0

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