import pytest
import json
import factory
import sys
from .factories import UserRoleFactory, UsersFactory
from core.models import User, UserRole
sys.path.append('..')
from api.view import UserViewSet, UserRoleViewSet
from .fixtures import api_client, get_token
from .default_tests import default_test_delete, default_test_list, default_test_retrieve, default_test_not_found, \
    default_test_not_authorized

pytestmark = pytest.mark.django_db  # Links with django data base


# Tests for user roles
class TestUserRole:
    endpoint = '/user_roles/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=UserRoleFactory, endpoint=self.endpoint, viewset=UserRoleViewSet,
                          get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=UserRoleFactory, endpoint='user_role', viewset=UserRoleViewSet,
                              get_token=get_token)


# Tests for users
class TestUser:
    endpoint = '/users/'  # Needed endpoints

    def test_list(self, rf, get_token):  # <----------Tests list-view
        default_test_list(api_client=rf, factory=UsersFactory, endpoint=self.endpoint, viewset=UserViewSet, get_token=get_token)

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        default_test_retrieve(api_client=rf, factory=UsersFactory, endpoint='user', viewset=UserViewSet,
                              foreign_keys={'role': UserRole}, get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/user', factory=UsersFactory(), model=User,
                            get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, model=User, viewset=UserViewSet, factory=UsersFactory,
                               endpoint='user', get_token=get_token)

    def test_not_authenticated(self, api_client):
        default_test_not_authorized(api_client=api_client, model=User, factory=UsersFactory, endpoint='user')

    def test_create(self, mocker, rf, get_token):  # <----------Tests creating an instance functionality
        valid_data_dict = factory.build(
            dict,
            FACTORY_CLASS=UsersFactory
        )  # Creates dictionary with data of the model

        UserRoleFactory.create_batch(4)
        valid_data_dict['role'] = valid_data_dict['role'].role

        request = rf.post(
            path=self.endpoint,
            content_type='application/json',
            data=json.dumps(valid_data_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = UserViewSet.as_view({'post': 'create'})
        response = view(request).render()

        # Deleting password from the dict, because response does not return password
        del valid_data_dict['password']

        # Testing if results are equal
        assert response.status_code == 200 or response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_update(self, mocker, rf, get_token):   # <----------Tests updating an instance functionality
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

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_user.id}',
            content_type='application/json',
            data=json.dumps(user_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
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