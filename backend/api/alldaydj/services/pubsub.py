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

from google.cloud import pubsub_v1

from firebase_admin import credentials, firestore, initialize_app
from os import environ
from typing import Dict

TOPIC_VALIDATE = environ.get("ALLDADYJ_TOPIC_VALIDATE")

pubsub_creds = credentials.Certificate(environ.get("FIREBASE_CREDENTIALS"))
publisher = pubsub_v1.PublisherClient(credentials=pubsub_creds)
