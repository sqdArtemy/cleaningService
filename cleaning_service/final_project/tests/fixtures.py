import json

import pytest
from rest_framework.test import APIClient

from core.models import User, UserRole


@pytest.fixture
def get_token():
    client = APIClient()
    # Creating test user for authentication
    test_role = UserRole.objects.create(role='test')
    test_user = User.objects.create_user(email='123@gmail.com', password='Admin123!', username='1', phone=123, name=1,
                                         role=test_role)

    # Getting token
    response = client.post("/auth/jwt/create", {"email": test_user.email, "password": "Admin123!"})
    response_content = json.loads(response.content.decode('utf-8'))
    token = response_content["access"]

    return token

@pytest.fixture  # Let us interact with DRF endpoints
def api_client():
    client = APIClient()
    return client

