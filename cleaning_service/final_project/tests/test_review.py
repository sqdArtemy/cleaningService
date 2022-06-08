import json
import pytest

from django.utils import timezone

from core.models import Review, User

from .factories import ReviewFactory
from api.view import ReviewViewSet
from .default_tests import (default_test_create, default_test_delete, default_test_list, default_test_not_authorized,
                            default_test_not_found, default_test_retrieve)
from .fixtures import api_client, get_token

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for reviews
class TestReview:
    endpoint = '/reviews/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=ReviewFactory, endpoint=self.endpoint, viewset=ReviewViewSet,
                          get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=ReviewFactory, endpoint='review', viewset=ReviewViewSet,
                              foreign_keys={'customer': User}, has_date=True, get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/review', factory=ReviewFactory(), model=Review,
                            get_token=get_token)

    def test_create(self, api_client, get_token):  # <----------Tests creating an instance functionality
        default_test_create(api_client=api_client, endpoint=self.endpoint, factory=ReviewFactory, model=Review,
                            foreign_keys={'customer': User}, has_date=True, get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=ReviewViewSet, factory=ReviewFactory,
                               endpoint='review', get_token=get_token)

    def test_not_authenticated(self, api_client):
        default_test_not_authorized(api_client=api_client, factory=ReviewFactory, endpoint='review')

    def test_update(self, mocker, rf, get_token):   # <----------Tests updating an instance functionality
        old_review = ReviewFactory()
        new_review = ReviewFactory()

        review_dict = {
            'feedback': new_review.feedback,
            'rate': new_review.rate,
            'created_at': old_review.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'customer': old_review.customer.username,
            'request': old_review.request.id,
        }

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_review.id}',
            content_type='application/json',
            data=review_dict,
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = ReviewViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_review.id).render()

        review_dict['id'] = old_review.id  # Adding id to expected output. Did not add it before because objects

        assert response.status_code == 200
        assert response.data == review_dict
