"""
    Test utility functions.
"""

from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APIClient


def get_bearer_token(username: str, password: str, host: str, client: APIClient) -> str:
    """Obtains a current bearer token for a given user.

    Args:
        username (str): The user to log in as.
        password (str): Their password.
        host (str): The hostname to make the request for.
        client (APIClient): The test client to use for login.

    Returns:
        str: The bearer token (if we can get it).
    """

    url = reverse("token_obtain_pair")
    auth_request = {"email": username, "password": password}
    response = client.post(url, auth_request, format="json", **{"HTTP_HOST": host})

    if response.status_code == status.HTTP_200_OK:
        json_response = json.loads(response.content)
        return json_response["access"]
    else:
        pass
