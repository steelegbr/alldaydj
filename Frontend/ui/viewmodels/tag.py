from models.dto.audio import Tag
from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtWidgets import QMessageBox
from services.factory import TagService, ServiceFactory
from typing import List


class TagListModel(QAbstractListModel):
    __tags: List[Tag]
    __tag_service: TagService

    def __init__(
        self,
        *args,
        tags=None,
        tag_service: TagService = ServiceFactory().tagService(),
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__tag_service = tag_service
        self.__tags = tags or []
        self.refresh()

    def refresh(self):
        self.__tag_service.get_all_tags(self.__update_tags, self.__handle_failure)

    def __update_tags(self, tags: List[Tag]):
        self.beginResetModel()
        self.__tags = tags
        self.endResetModel()

    def __handle_failure(self, error: str):
        pass

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.__tags[index.row()].tag

    def rowCount(self, index):
        return len(self.__tags)

    def addTag(self, tag: str):
        if not tag:
            return

        existing_tags = [
            existing_tag for existing_tag in self.__tags if existing_tag.tag == tag
        ]
        if not existing_tags:
            self.__tag_service.add_tag(
                tag, self.__handle_tag_action, self.__handle_failure
            )

    def __handle_tag_action(self, tag: Tag):
        self.refresh()
