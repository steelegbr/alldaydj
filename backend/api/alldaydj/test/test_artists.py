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


@parameterized.expand(
    [("Artist 1", "Artist 2"), ("Artist-3", "Artist-4"), ("Artist?5", "Artist?6")]
)
def test_update_artist(original_name: str, new_name: str):
    # Create original artist

    post_response = client.post("/api/artist/", json={"name": original_name})
    assert post_response.status_code == 200
    post_response_json = post_response.json()
    assert post_response_json["name"] == original_name

    # Perform the update

    url = f"/api/artist/{post_response_json['id']}"
    put_response = client.put(url, json={"name": new_name})
    print(put_response.content)
    assert put_response.status_code == 200

    # Check

    get_response = client.get(url)
    get_response_json = get_response.json()
    assert get_response.status_code == 200
    assert get_response_json["name"] == new_name

    # Delete

    delete_response = client.delete(url)
    assert delete_response.status_code == 204


def test_rename_collision():
    # Arrange

    original_response = client.post("/api/artist/", json={"name": "Colliding Artist 1"})
    original_response_json = original_response.json()

    second_response = client.post("/api/artist/", json={"name": "Colliding Artist 2"})
    second_response_json = second_response.json()

    # Act

    rename_response = client.put(
        f"/api/artist/{second_response_json['id']}", json={"name": "Colliding Artist 1"}
    )

    # Assert

    assert original_response.status_code == 200
    assert second_response.status_code == 200
    assert rename_response.status_code == 409

    # Cleanup

    client.delete(f"/api/artist/{original_response_json['id']}")
    client.delete(f"/api/artist/{second_response_json['id']}")


def test_create_collision():
    # Arrange

    original_response = client.post("/api/artist/", json={"name": "Colliding Artist"})
    original_response_json = original_response.json()

    # Act

    second_response = client.post("/api/artist/", json={"name": "Colliding Artist"})

    # Assert

    assert original_response.status_code == 200
    assert second_response.status_code == 409

    # Cleanup

    client.delete(f"/api/artist/{original_response_json['id']}")
