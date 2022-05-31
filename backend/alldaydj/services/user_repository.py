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

from alldaydj.models.user import User
from alldaydj.services.cryptography import verify_password
from alldaydj.services.database import db
from alldaydj.services.logging import logger
from alldaydj.services.repository import Repository
from hashlib import sha256

COLLECTION_USER = "users"


class UserRepository(Repository):
    def __map_doc_to_user(self, user_doc) -> User:
        return User.parse_obj({**user_doc.to_dict(), "id": user_doc.id})

    def email_to_id(self, email: str) -> str:
        encoded_email = email.encode("utf-8")
        return sha256(encoded_email).hexdigest()

    def get(self, email: str) -> User:
        logger.info(f"Lookup for user email {email}")
        return self.get_document(
            self.email_to_id(email), COLLECTION_USER, self.__map_doc_to_user
        )

    def save(self, user: User):
        logger.info(f"Saving user email {user.email}")
        self.save_stripped_document(self.email_to_id(user.email), COLLECTION_USER, user)

    def delete(self, email: str):
        logger.info(f"Delete user with email {email}")
        db.collection(COLLECTION_USER).document(self.email_to_id(email)).delete()

    def authenticate(self, email: str, password: str):
        logger.info(f"Authentication attempt for user email {email}")
        if user := self.get(email):
            return verify_password(password, user.password)
