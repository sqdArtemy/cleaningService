import pytest
import json
import sys
from .factories import ReviewFactory
from core.models import Review, User
sys.path.append('..')
from api.view import ReviewViewSet
from .fixtures import api_client, get_token
from .default_tests import default_test_delete, default_test_list, default_test_retrieve, default_test_create, \
    default_test_not_found, default_test_not_authorized

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
        default_test_not_found(api_client=rf, model=Review, viewset=ReviewViewSet, factory=ReviewFactory,
                               endpoint='review', get_token=get_token)

    def test_not_authenticated(self, api_client):
        default_test_not_authorized(api_client=api_client, model=Review, factory=ReviewFactory, endpoint='review')

    def test_update(self, mocker, rf, get_token):   # <----------Tests updating an instance functionality
        old_review = ReviewFactory()
        new_review = ReviewFactory()
        request_dict = {
            'feedback': new_review.feedback,
            'rate': new_review.rate,
            'created_at': json.dumps(new_review.created_at, indent=4, sort_keys=True, default=str),
            'customer': old_review.customer.username,
            'request': old_review.request.id,
        }

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_review.id}',
            content_type='application/json',
            data=json.dumps(request_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        # Mocking
        mocker.patch.object(ReviewViewSet, 'get_object', return_value=old_review)
        mocker.patch.object(Review, 'save')

        view = ReviewViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_review.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == request_dict