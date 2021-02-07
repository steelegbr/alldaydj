"""
    Test utility functions.
"""

from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APIClient
from typing import List, Tuple


def set_bearer_token(username: str, password: str, client: APIClient) -> None:
    """Attempts to set the current bearer token for a given user.

    Args:
        username (str): The user to log in as.
        password (str): Their password.
        client (APIClient): The test client to use for login.
    """

    url = reverse("token_obtain_pair")
    auth_request = {"username": username, "password": password}
    response = client.post(url, auth_request, format="json")

    if response.status_code == status.HTTP_200_OK:
        json_response = json.loads(response.content)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {json_response['access']}")
