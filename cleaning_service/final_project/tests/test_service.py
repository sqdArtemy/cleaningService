import json
import sys

import pytest

from core.models import Category, Service, User

from .factories import CategoryFactory, ServiceFactory
from .fixtures import api_client, get_token

sys.path.append('..')
from api.view import CategoryViewSet, ServiceViewSet

from .default_tests import (default_test_create, default_test_delete, default_test_list, default_test_not_authorized,
                            default_test_not_found, default_test_retrieve)

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for user roles
class TestCategory:
    endpoint = '/categories/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=CategoryFactory, endpoint=self.endpoint, viewset=CategoryViewSet,
                          get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, viewset=CategoryViewSet, endpoint='category', factory=CategoryFactory,
                              get_token=get_token)


# Tests for users
class TestService:
    endpoint = '/services/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=ServiceFactory, endpoint=self.endpoint, viewset=ServiceViewSet,
                          get_token=get_token)

    def test_retrieve(self, mocker, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=ServiceFactory, endpoint='service', get_token=get_token,
                              viewset=ServiceViewSet, foreign_keys={'category': Category})

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='service', factory=ServiceFactory, model=Service,
                            get_token=get_token)

    def test_create(self, api_client, get_token):  # <----------Tests creating an instance functionality
        default_test_create(api_client=api_client, endpoint=self.endpoint, factory=ServiceFactory, model=Service,
                            foreign_keys={'category': Category}, get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=ServiceViewSet, factory=ServiceFactory, endpoint='service',
                               get_token=get_token)

    def test_not_authenticated(self, api_client):
        default_test_not_authorized(api_client=api_client, factory=ServiceFactory, endpoint='service')

    def test_update(self, rf, get_token):   # <----------Tests updating an instance functionality
        old_service = ServiceFactory()
        new_service = ServiceFactory()
        service_dict = {
            'name': new_service.name,
            'category': new_service.category.naming,
            'picture': str(new_service.picture),
            'description': new_service.description,
        }

        # Setting new unique name to a service in order to avoid errors
        new_service.name = 'new_unique_name'
        new_service.save()

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_service.id}',
            content_type='application/json',
            data=json.dumps(service_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = ServiceViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_service.id).render()

        # Adding core media folder to expected json
        service_dict['picture'] = '/media/' + service_dict['picture']

        service_dict['id'] = old_service.id  # Adding id to expected output. Did not add it before because objects

        assert response.status_code == 200
        assert json.loads(response.content) == service_dict
