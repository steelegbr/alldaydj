"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
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

from fastapi.testclient import TestClient
from main import app
from parameterized import parameterized

client = TestClient(app)


@parameterized.expand(
    [
        ("Normal Looking Artist",),
        ("Füññy Lööking Chàràçtèrß",),
        ("📻📡 🎶",),
    ]
)
def test_can_create_retrieve_delete_artist(name: str):
    # Create

    post_response = client.post("/api/artist/", json={"name": name})
    assert post_response.status_code == 200
    post_response_json = post_response.json()
    assert post_response_json["name"] == name

    # Retrieve

    url = f"/api/artist/{post_response_json['id']}"
    get_response = client.get(url)
    assert get_response.status_code == 200
    get_response_json = get_response.json()
    assert get_response_json["name"] == name

    # Delete

    delete_response = client.delete(url)
    assert delete_response.status_code == 204
