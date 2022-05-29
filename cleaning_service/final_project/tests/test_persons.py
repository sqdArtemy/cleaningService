import pytest
import json
import factory
import sys
from rest_framework.test import APIClient
from rest_framework import permissions
from .factories import UserRoleFactory, UsersFactory
from core.models import User, UserRole
sys.path.append('..')
from api.view import UserViewSet, UserRoleViewSet
from .default_tests import default_test_delete, default_test_list, default_test_retrieve


pytestmark = pytest.mark.django_db  # Links with django data base


@pytest.fixture  # Let us interact with DRF endpoints
def api_client():
    client = APIClient()
    #client.credentials(HTTP_AUTHORIZATION='Bearer ' + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNzQxMDUyLCJpYXQiOjE2NTM3NDA3NTIsImp0aSI6ImVjYzlmMzEyZmYzOTRhN2JiNGI3ZTRlMzAyMTJlZjJlIiwidXNlcl9pZCI6Mn0.ltbGE9izxeB4cH1nifpfTz6SQjcSfTXt-Gd13O_ypEs")
    return client

# Tests for user roles
class TestUserRole:
    endpoint = '/user_roles/'  # Needed endpoints
    UserRoleViewSet.permission_classes = (permissions.AllowAny,)

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=UserRoleFactory, endpoint=self.endpoint, viewset=UserRoleViewSet)

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=UserRoleFactory, endpoint='user_role', viewset=UserRoleViewSet)


# Tests for users
class TestUser:
    UserViewSet.permission_classes = (permissions.AllowAny,)
    endpoint = '/users/'  # Needed endpoints

    def test_list(self, rf):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=UsersFactory, endpoint=self.endpoint, viewset=UserViewSet)

    def test_retrieve(self, rf):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=UsersFactory, endpoint='user', viewset=UserViewSet, foreign_keys={'role': UserRole})

    def test_delete(self, api_client):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/user', factory=UsersFactory(), model=User)

    def test_create(self, mocker, rf):  # <----------Tests creating an instance functionality
        valid_data_dict = factory.build(
            dict,
            FACTORY_CLASS=UsersFactory
        )  # Creates dictionary with data of the model

        UserRoleFactory.create_batch(4)
        valid_data_dict['role'] = valid_data_dict['role'].role

        request = rf.post(
            path=self.endpoint,
            content_type='application/json',
            data=json.dumps(valid_data_dict)
        )

        view = UserViewSet.as_view({'post': 'create'})
        response = view(request).render()

        # Deleting password from the dict, because response does not return password
        del valid_data_dict['password']

        # Testing if results are equal
        assert response.status_code == 200 or response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf):   # <----------Tests updating an instance functionality
        old_user = UsersFactory()
        new_user = UsersFactory()
        user_dict = {
            'name': new_user.name,
            'username': new_user.username,
            'phone': new_user.phone,
            'email': old_user.email,
            'role': old_user.role.role,
            'password': new_user.password,
        }

        UserRole.objects.create(role=old_user.role)  # Recreating user role in DB

        url = f'{self.endpoint[0:-2]}/{old_user.id}'
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(user_dict)
        )

        # Mocking
        mocker.patch.object(UserViewSet, 'get_object', return_value=old_user)
        mocker.patch.object(User, 'save')

        view = UserViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_user.id).render()

        # Deleting password from the dict, because response does not return password
        del user_dict['password']

        assert response.status_code == 200
        assert json.loads(response.content) == user_dict