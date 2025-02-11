from models.dto.audio import Tag
from PySide6.QtCore import QAbstractListModel, Qt
from services.factory import ServiceFactory, TagService
from services.logging import Logger, LoggingService
from typing import List


class TagListModel(QAbstractListModel):
    __logger: Logger
    __tags: List[Tag]
    __tag_service: TagService

    def __init__(
        self,
        *args,
        tags=None,
        log_service: LoggingService = LoggingService(),
        tag_service: TagService = ServiceFactory().tagService(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.__logger = log_service.get_logger(__name__)
        self.__tag_service = tag_service
        self.__tags = tags or []
        self.refresh()

    def refresh(self):
        self.__tag_service.get_all(self.__update_tags, self.__handle_failure)

    def __update_tags(self, tags: List[Tag]):
        self.beginResetModel()
        self.__tags = tags
        self.endResetModel()

    def __handle_failure(self, error: str):
        self.__logger.error(f"Failed reported back to tag viewmodel: {error}")

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
            self.__tag_service.add(tag, self.__handle_tag_action, self.__handle_failure)

    def deleteTag(self, index: int):
        if index < 0 or index >= len(self.__tags):
            return

        tag = self.__tags[index]

        self.__tag_service.delete(tag, self.__handle_none_action, self.__handle_failure)

    def __handle_tag_action(self, tag: Tag):
        self.refresh()

    def __handle_none_action(self):
        self.refresh()
