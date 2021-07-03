"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
