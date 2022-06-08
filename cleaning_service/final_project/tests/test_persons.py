import json
import sys

import factory
import pytest

from core.models import Category, User, UserRole

from .default_tests import (default_test_delete, default_test_list, default_test_not_authorized,
                            default_test_not_found, default_test_retrieve)

from .factories import ServiceFactory, UserRoleFactory, UsersFactory
from django.forms.models import model_to_dict
from .fixtures import api_client, get_token
from api.view.profiles import UserRoleViewSet, UserViewSet, create

pytestmark = pytest.mark.django_db  # Links with django data base


# Function, which formats services in user tests
def service_formatter(services):
    # Formatting services field for output
    formated_services = []
    for srv in services:
        srv = model_to_dict(srv)
        srv['category'] = str(Category.objects.get(id=srv['category']))
        srv['hours_required'] = int(srv['hours_required'])
        srv['picture'] = '/media/' + str(srv['picture'])
        formated_services.append(srv)
    return formated_services


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
        default_test_list(api_client=rf, factory=UsersFactory, endpoint=self.endpoint, viewset=UserViewSet,
                          get_token=get_token)

    def test_delete(self, api_client, get_token):  # <----------Tests deleting functionality
        default_test_delete(api_client=api_client, endpoint='/user', factory=UsersFactory(), model=User,
                            get_token=get_token)

    def test_not_found(self, rf, get_token):  # <----------Tests case if object is not found
        default_test_not_found(api_client=rf, viewset=UserViewSet, factory=UsersFactory,
                               endpoint='user', get_token=get_token)

    def test_not_authenticated(self, api_client):  # <----------Tests if user is not authenticated
        default_test_not_authorized(api_client=api_client, factory=UsersFactory, endpoint='user')

    def test_retrieve(self, rf, get_token):  # <----------Tests getting only 1 item
        # Arrange
        user = UsersFactory()
        request = rf.get(f'/{self.endpoint}/{user.id}', {}, HTTP_AUTHORIZATION='Bearer {}'.format(get_token))

        # converts model instance into expected fields
        expected_json = model_to_dict(instance=user, exclude=("password", "is_active", 'is_staff', 'is_superuser',
                                                              'last_login', 'groups', 'user_permissions'))

        # Formatting data in proper way
        expected_json['picture'] = str(expected_json['picture'])
        expected_json['role'] = str(UserRole.objects.get(id=expected_json['role']))

        view = UserViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=user.id).render()

        expected_json['id'] = user.id  # Adding id to expected output. Did not add it before because objects
        expected_json['picture'] = None  # Setting None value instead of blank field

        # Comparing results
        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_create(self, rf, get_token):  # <----------Tests creating an instance functionality
        valid_data_dict = factory.build(
            dict,
            FACTORY_CLASS=UsersFactory
        )  # Creates dictionary with data of the model

        UserRoleFactory.create_batch(4)
        valid_data_dict['role'] = valid_data_dict['role'].role  # Formatting role field

        services = ServiceFactory.create_batch(2)
        valid_data_dict['services'] = [services[0].name, services[1].name]  # Formatting service field

        request = rf.post(  # Creating request to perform POST action
            path=self.endpoint,
            content_type='application/json',
            data=json.dumps(valid_data_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = create
        response = view(request).render()
        json_response = json.loads(response.content)

        del valid_data_dict['password']  # Deleting password from the dict, because response does not return password
        del json_response['id']  # Deleting id from loads because id is PK, and they are going to be different
        valid_data_dict['services'] = service_formatter(services)  # Formatting services

        from pprint import pprint
        pprint(json_response)
        pprint(valid_data_dict)

        # Testing if results are equal
        assert response.status_code == 200 or response.status_code == 201
        assert json_response == valid_data_dict

    def test_update(self, rf, get_token):  # <----------Tests updating an instance functionality
        services = ServiceFactory.create_batch(2)  # Creating services for many to many field
        old_user = UsersFactory(services=(services[0].id, services[1].id))
        new_user = UsersFactory(services=(services[0].id, services[1].id))
        user_dict = {
            'name': new_user.name,
            'username': new_user.username,
            'phone': new_user.phone,
            'email': new_user.email,
            'country': new_user.country,
            'city': new_user.city,
            'services': (services[0].name, services[1].name,),
            'address_details': new_user.address_details,
            'role': new_user.role.role,
            'password': new_user.password,
            'rating': new_user.rating,
            'picture': str(new_user.picture),
            'users_rated': new_user.users_rated,
        }
        # Setting unique parameters to avoid unique constraint error
        new_user.username = 'unique_name'
        new_user.email = 'uniqueemail@gmail.com'
        new_user.save()

        request = rf.put(
            path=f'{self.endpoint[0:-2]}/{old_user.id}',
            content_type='application/json',
            data=json.dumps(user_dict),
            HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
        )

        view = UserViewSet.as_view({'put': 'update'})
        response = view(request, pk=old_user.id).render()

        user_dict['services'] = service_formatter(services)  # Formatting services
        user_dict['id'] = old_user.id  # Adding id to expected output. Did not add it before because objects

        # Deleting password from the dict, because response does not return password
        del user_dict['password']
        # If user has no picture - format empty field
        if len(user_dict['picture']) == 0:
            user_dict['picture'] = None

        assert response.status_code == 200
        assert json.loads(response.content) == user_dict
