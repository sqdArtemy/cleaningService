import json

import pytest

from core.models import Request, RequestStatus, Service, User

from .factories import RequestFactory, RequestStatusFactory
from .fixtures import api_client, get_token
from django.db.models.signals import post_save
from api.signals import company_notifier_signal
from api.view import RequestStatusViewSet, RequestViewSet

from .default_tests import (default_test_create, default_test_delete,
                            default_test_list, default_test_not_found,
                            default_test_retrieve)

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for user roles
class TestRequestStatus:
    endpoint = '/request_statuses/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=RequestStatusFactory, get_token=get_token,
                          endpoint=self.endpoint, viewset=RequestStatusViewSet)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=RequestStatusFactory, endpoint='request_status',
                              viewset=RequestStatusViewSet, get_token=get_token)


# Tests for users
class TestRequest:
    endpoint = '/requests/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=RequestFactory, endpoint=self.endpoint, viewset=RequestViewSet,
                          get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=RequestFactory, endpoint='request', viewset=RequestViewSet,
                              foreign_keys={'customer': User, 'status': RequestStatus, 'service': Service,
                                            'company': User}, get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='request', factory=RequestFactory, model=Request,
                            get_token=get_token)

    def test_create(self, api_client, get_token):  # <----------Tests creating an instance functionality
        default_test_create(api_client=api_client, endpoint=self.endpoint, factory=RequestFactory, model=Request,
                            foreign_keys={'customer': User, 'status': RequestStatus, 'service': Service},
                            get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=RequestViewSet, factory=RequestFactory,
                               endpoint='request', get_token=get_token)

    def test_update(self, rf, get_token):  # <----------Tests updating an instance functionality
        post_save.disconnect(sender=Request, receiver=company_notifier_signal)
        old_request = RequestFactory()
        new_request = RequestFactory()
        request_dict = {
            'status': new_request.status.status,
            'customer': old_request.customer.username,
            'service': old_request.service.name,
            'total_area': new_request.total_area,
            'address_details': new_request.address_details,
            'city': new_request.city,
            'country': new_request.country,
            'company': new_request.company.username,
            'min_rating_needed': new_request.min_rating_needed,
            'max_meter_cost': new_request.max_meter_cost,
        }

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_request.id}',
            content_type='application/json',
            data=json.dumps(request_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = RequestViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_request.id).render()

        json_response = json.loads(response.content)
        # Deleting total cost because it depends on a service which is different in both cases
        del json_response['total_cost']
        request_dict['id'] = old_request.id  # Adding id to expected output. Did not add it before because objects

        assert response.status_code == 200
        assert json_response == request_dict
