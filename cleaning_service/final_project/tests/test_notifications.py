import json

import pytest

from api.view import NotificationViewSet
from core.models import Notification, Request, User

from .default_tests import (default_test_create, default_test_delete,
                            default_test_list, default_test_not_found,
                            default_test_retrieve)
from .factories import NotificationFactory
from .fixtures import api_client, get_token

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for notification
class TestNotification:
    endpoint = '/notifications/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=NotificationFactory, endpoint=self.endpoint,
                          viewset=NotificationViewSet, get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=NotificationFactory, endpoint='notification',
                              viewset=NotificationViewSet, foreign_keys={'user': User},
                              get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/notification', factory=NotificationFactory(),
                            model=Notification, get_token=get_token)

    def test_create(self, api_client, get_token):  # <----------Tests creating an instance functionality
        default_test_create(api_client=api_client, endpoint=self.endpoint, factory=NotificationFactory,
                            model=Notification, foreign_keys={'user': User}, get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=NotificationViewSet, factory=NotificationFactory,
                               endpoint='notification', get_token=get_token)

    def test_update(self, rf, get_token):  # <----------Tests updating an instance functionality
        old_notification = NotificationFactory()
        new_notification = NotificationFactory()
        notification_dict = {
            'user': old_notification.user.username,
            'request': old_notification.request.id,
            'seen': new_notification.seen,
            'accepted': new_notification.accepted,
            'text': old_notification.text,
            'header': old_notification.header,
        }

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{new_notification.id}',
            content_type='application/json',
            data=json.dumps(notification_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = NotificationViewSet.as_view({'put': 'partial_update'})
        response = view(request, pk=old_notification.id).render()

        # Adding id to expected output. Did not add it before because objects
        notification_dict['id'] = old_notification.id

        assert response.status_code == 200
        assert json.loads(response.content) == notification_dict
