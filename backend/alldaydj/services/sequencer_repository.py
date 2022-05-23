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

from alldaydj.models.sequencer import CartIdSequencer
from alldaydj.services.database import db
from alldaydj.services.logging import logger
from alldaydj.services.repository import Repository
from typing import List, Optional
from uuid import UUID

COLLECTION_SEQUENCER = "sequencers"


class SequencerRepository(Repository):
    def __map_doc_to_sequencer(self, seq_doc) -> CartIdSequencer:
        return CartIdSequencer.parse_obj({**seq_doc.to_dict(), "id": seq_doc.id})

    def get(self, id: UUID) -> Optional[CartIdSequencer]:
        logger.info(f"Lookup for sequencer ID {id}")
        return self.get_document(id, COLLECTION_SEQUENCER, self.__map_doc_to_sequencer)

    def get_by_name(self, name: str) -> List[CartIdSequencer]:
        return [
            self.__map_doc_to_sequencer(seq_doc)
            for seq_doc in db.collection(COLLECTION_SEQUENCER).where("name", "==", name)
        ]

    def all(self) -> List[CartIdSequencer]:
        logger.info("Lookup for all sequencers")
        return self.get_all(COLLECTION_SEQUENCER, self.__map_doc_to_sequencer)

    def save(self, id: UUID, seq: CartIdSequencer):
        logger.info(f"Saving sequencer {id}")
        self.save_stripped_document(id, COLLECTION_SEQUENCER, seq)

    def delete(self, id: UUID):
        logger.info(f"Deleting sequencer {id}")
        db.collection(COLLECTION_SEQUENCER).document(str(id)).delete()
