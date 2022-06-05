import json

from django.forms.models import model_to_dict

from core.models import Request, User

from .factories import UserRoleFactory, UsersFactory


# Template function in order to test list view
def default_test_list(api_client, factory, endpoint, viewset, get_token):
    amount = 10
    factory.create_batch(amount)  # Creates 10 random objects

    request = api_client.get(endpoint, HTTP_AUTHORIZATION='Bearer {}'.format(get_token))

    view = viewset.as_view({'get': 'list'})
    response = view(request).render()

    # Add 1 to the counter because of AUTH user account
    if factory == UsersFactory or factory == UserRoleFactory: amount += 1

    # Comparing results
    assert response.status_code == 200
    assert len(json.loads(response.content)) == amount


# Template function for testing delete
def default_test_delete(api_client, factory, endpoint, model, get_token):
    # Arrange
    amount = 0
    if model == User: amount += 1
    object = factory

    response = api_client.delete(f'{endpoint}/{object.id}', HTTP_AUTHORIZATION='Bearer {}'.format(get_token))

    # Comparing results
    assert response.status_code == 204
    assert model.objects.all().count() == amount


# Template test for retrieve functionality
def default_test_retrieve(api_client, factory, endpoint, viewset, get_token, foreign_keys=None, has_date=None):
    # Arrange
    object = factory()
    request = api_client.get(f'/{endpoint}/{object.id}', {}, HTTP_AUTHORIZATION='Bearer {}'.format(get_token))

    # converts model instance into expected fields
    expected_json = model_to_dict(instance=object, exclude=("id", "password", "is_active", 'is_staff', 'is_superuser',
                                                            'last_login', 'groups', 'user_permissions'))

    # If model has a picture => refactor it to appropriate format
    if 'picture' in expected_json: expected_json['picture'] = str(expected_json['picture'])

    if foreign_keys is not None:  # Substituting foreign keys ID`s with serializer`s representation
        for item in foreign_keys.keys():
            expected_json[item] = str(foreign_keys[item].objects.get(id=expected_json[item]))

    view = viewset.as_view({'get': 'retrieve'})
    response = view(request, pk=object.id).render()

    json_response = json.loads(response.content)

    if has_date is not None:  # Formatting timedate field
        json_response['created_at'] = json.dumps(json_response['created_at'], indent=4, sort_keys=True, default=str)
        json_response['created_at'] = json_response['created_at'].replace('Z', '').replace('T', " ")
        expected_json['created_at'] = json.dumps(expected_json['created_at'], indent=4, sort_keys=True, default=str)

    # Adding media root to expected output
    if 'picture' in expected_json: expected_json['picture'] = 'http://testserver/media/' + str(expected_json['picture'])

    # Comparing results
    assert response.status_code == 200
    assert json_response == expected_json

def default_test_create(api_client, factory, endpoint, model, get_token, foreign_keys=None, has_date=None):
    obj = factory()

    expected_json = model_to_dict(instance=obj, exclude="id")
    expected_json['no_signal'] = 'no_signal'  # Adding marker to disable signals

    # If model has a picture => refactor it to appropriate format
    if 'picture' in expected_json: expected_json['picture'] = str(expected_json['picture'])

    # Formatting date
    if has_date is not None:
        date = json.dumps(obj.created_at, indent=4, sort_keys=True, default=str)
        expected_json['created_at'] = date.replace(' ', 'T').replace('"', '') + 'Z'

    if foreign_keys is not None:  # Substituting foreign keys ID`s with serializer`s representation
        for item in foreign_keys.keys():
            expected_json[item] = str(foreign_keys[item].objects.get(id=expected_json[item]))

    response = api_client.post(
        path=endpoint,
        data=expected_json,
        format='json',
        HTTP_AUTHORIZATION='Bearer {}'.format(get_token)
    )
    if model == Request: expected_json['company'] = None  # When request created this field should be empty

    # Adding media root to expected output
    if 'picture' in expected_json: expected_json['picture'] = '/media/' + str(expected_json['picture'])

    del expected_json['no_signal']  # Removing marker
    expected_json
    # Comparing results
    assert response.status_code == 200
    assert json.loads(response.content) == expected_json
    assert model.objects.count() == 2


# Default test for cse if object is not found
def default_test_not_found(api_client, factory, endpoint, viewset, get_token):
    obj = factory()
    request = api_client.get(f'/{endpoint}/{obj.id}', HTTP_AUTHORIZATION='Bearer {}'.format(get_token))

    expected_json = model_to_dict(instance=obj)

    view = viewset.as_view({'get': 'retrieve'})
    response = view(request, pk=(obj.id + 1)).render()

    assert response.status_code == 404

# Default test for case, when user is not authenticated
def default_test_not_authorized(api_client, factory, endpoint):
    object = factory()

    response = api_client.delete(f'/{endpoint}/{object.id}')

    # Comparing results
    assert response.status_code == 401


