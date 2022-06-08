import json
import pytest

from core.models import Order, Notification

from .factories import OrderFactory
from api.view import OrderViewSet

from .default_tests import (default_test_create, default_test_delete, default_test_list, default_test_not_authorized,
                            default_test_not_found, default_test_retrieve)
from .fixtures import api_client, get_token

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for reviews
class TestOrder:
    endpoint = '/orders/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=OrderFactory, endpoint=self.endpoint, viewset=OrderViewSet,
                          get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='order', factory=OrderFactory, model=Order,
                            get_token=get_token)

    def test_create(self, api_client, get_token):  # <----------Tests creating an instance functionality
        default_test_create(api_client=api_client, endpoint=self.endpoint, factory=OrderFactory, model=Order,
                            get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=OrderViewSet, factory=OrderFactory,
                               endpoint='order', get_token=get_token)

    def test_not_authenticated(self, api_client):
        default_test_not_authorized(api_client=api_client, factory=OrderFactory, endpoint='review')

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=OrderFactory, endpoint='order', viewset=OrderViewSet,
                              get_token=get_token)

    def test_update(self, rf, get_token):   # <----------Tests updating an instance functionality
        old_order = OrderFactory()
        new_order = OrderFactory()
        order_dict = {
            'notification': old_order.notification.id,
            'accepted': new_order.accepted,
            'total_cost': old_order.total_cost,
            'company': old_order.notification.user.username,
            'request': old_order.request.id
        }

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_order.id}',
            content_type='application/json',
            data=json.dumps(order_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = OrderViewSet.as_view({'put': 'partial_update'})
        response = view(request, pk=old_order.id).render()

        # Adding id to expected output. Did not add it before because objects
        order_dict['id'] = old_order.id

        assert response.status_code == 200
        assert json.loads(response.content) == order_dict
