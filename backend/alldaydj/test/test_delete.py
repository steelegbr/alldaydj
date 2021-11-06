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

from rest_framework.test import APITestCase
from unittest.mock import call, patch

from alldaydj.models import Cart
from alldaydj.signals.handlers import delete_audio


class DeleteTest(APITestCase):
    """
    Tests files are deleted from storage.
    """

    @patch("django.core.files.storage.default_storage.exists")
    @patch("django.core.files.storage.default_storage.delete")
    def test_files_deleted(self, delete_mock, exists_mock):
        """
        Audio files are deleted if they exist.
        """

        exists_mock.side_effect = [True, False]
        expected_exists_calls = [call("audio/TEST123"), call("compressed/TEST123")]

        cart = Cart()
        cart.id = "TEST123"

        delete_audio(None, cart)

        self.assertEqual(exists_mock.call_count, 2)
        exists_mock.assert_has_calls(expected_exists_calls)

        self.assertEqual(delete_mock.call_count, 1)
        delete_mock.assert_called_with("audio/TEST123")
