import pytest
import json
import factory
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import ReviewFactory
from core.models import Review, User
sys.path.append('..')
from api.view import ReviewViewSet
from .default_tests import default_test_delete, default_test_list, default_test_retrieve
from django.forms.models import model_to_dict

pytestmark = pytest.mark.django_db  # Links with django data base


@pytest.fixture  # Let us interact with DRF endpoints
def api_client():
    client = APIClient()
    # client.credentials(HTTP_AUTHORIZATION='Bearer ' + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNzQwOTY0LCJpYXQiOjE2NTM3NDA2NjQsImp0aSI6ImUwOGI1NWIzYzk5YTQ5NTNiZjFlNmZjNjgwMzRlMmMxIiwidXNlcl9pZCI6Mn0.m1k2OJ8a559LUFyzem-qmEilQIn0lY7B9n4fYhqvJUQ")
    return client


# Tests for reviews
class TestReview:
    endpoint = '/reviews/'  # Needed endpoints
    ReviewViewSet.permission_classes = [permissions.AllowAny]

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=ReviewFactory,
                          endpoint=self.endpoint, viewset=ReviewViewSet)

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=ReviewFactory, endpoint='review', viewset=ReviewViewSet,
                              foreign_keys={'customer': User}, has_date=True)

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/review',
                            factory=ReviewFactory(), model=Review)

    def test_create(self, api_client):  # <----------Tests creating an instance functionality
        review = ReviewFactory()

        # Formatting date
        date = json.dumps(review.created_at, indent=4, sort_keys=True, default=str)
        date = date.replace(' ', 'T').replace('"', '') + 'Z'

        expected_json = {
            'feedback': review.feedback,
            'rate': review.rate,
            'customer': review.customer.username,
            'created_at': date,
            'request': review.request.id,
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
        old_review = ReviewFactory()
        new_review = ReviewFactory()
        request_dict = {
            'feedback': new_review.feedback,
            'rate': new_review.rate,
            'created_at': json.dumps(new_review.created_at, indent=4, sort_keys=True, default=str),
            'customer': old_review.customer.username,
            'request': old_review.request.id,
        }

        url = f'{self.endpoint[0:-2]}/{old_review.id}'
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(request_dict)
        )

        # Mocking
        mocker.patch.object(ReviewViewSet, 'get_object', return_value=old_review)
        mocker.patch.object(Review, 'save')

        view = ReviewViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_review.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == request_dict