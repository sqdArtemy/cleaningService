from rest_framework import permissions
import json
from django.forms.models import model_to_dict


# Template function in order to test list view
def default_test_list(api_client, factory, endpoint, viewset):
    factory.create_batch(10)  # Creates 10 random users

    request = api_client.get(endpoint)

    view = viewset.as_view({'get': 'list'})
    response = view(request).render()

    # Comparing results
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 10


# Template function for testing delete
def default_test_delete(api_client, factory, endpoint, model):
    # Arrange
    object = factory
    url = f'{endpoint}/{object.id}'

    response = api_client.delete(url)

    # Comparing results
    assert response.status_code == 204
    assert model.objects.all().count() == 0


# Template test for retrieve functionality
def default_test_retrieve(api_client, factory, endpoint, viewset, foreign_keys=None, has_date=None):
    # Arrange
    object = factory()
    url = f'/{endpoint}/{object.id}'
    request = api_client.get(url)

    # converts model instance into expected fields
    expected_json = model_to_dict(instance=object, exclude=("id", "password", "is_active", 'is_staff', 'is_superuser',
                                                            'last_login', 'groups', 'user_permissions'))

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

    # Comparing results
    assert response.status_code == 200
    assert json_response == expected_json
