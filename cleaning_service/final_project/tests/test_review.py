import pytest
import json
import factory
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import ReviewFactory
from core.models import Review
sys.path.append('..')
from api.view import ReviewViewSet

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

    def test_list(self, api_client):  # <----------Tests list-view
        ReviewFactory.create_batch(10)  # Creates 10 random users

        response = api_client.get(self.endpoint)

        # Comparing results
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10

    def test_retrieve(self, mocker, rf):  # <----------Tests getting only 1 item
        # Arrange
        review = ReviewFactory()
        url = f'{self.endpoint[0:-2]}/{review.id}'
        request = rf.get(url)

        expected_json = {  # Data for comparison
            'feedback': review.feedback,
            'rate': review.rate,
            'created_at': json.dumps(review.created_at, indent=4, sort_keys=True, default=str),
            'customer': review.customer.username,
            'request': review.request.id,
        }

        view = ReviewViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=review.id).render()

        # Formatting timedate field
        json_response = json.loads(response.content)
        json_response['created_at'] = json.dumps(json_response['created_at'], indent=4, sort_keys=True, default=str)
        json_response['created_at'] = json_response['created_at'].replace('Z', '').replace('T', " ")

        # Comparing results
        assert response.status_code == 200
        assert json_response == expected_json

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        # Arrange
        review = ReviewFactory()
        url = f'{self.endpoint[0:-2]}/{review.id}'

        response = api_client.delete(url)

        # Comparing results
        assert response.status_code == 204
        assert Review.objects.all().count() == 0

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