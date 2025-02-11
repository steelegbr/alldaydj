from models.dto.audio import CartType
from PySide6.QtCore import QAbstractListModel, Qt
from services.factory import CartTypeService, ServiceFactory
from services.logging import Logger, LoggingService
from typing import List


class CartTypeListModel(QAbstractListModel):
    __cart_type_service: CartTypeService
    __logger: Logger
    __types: List[CartType]

    def __init__(
        self,
        *args,
        cart_types=None,
        cart_type_service: CartTypeService = ServiceFactory().cartTypeService(),
        log_service: LoggingService = LoggingService(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.__logger = log_service.get_logger(__name__)
        self.__cart_type_service = cart_type_service
        self.__types = cart_types or []
        self.refresh()

    def refresh(self):
        self.__cart_type_service.get_all(
            self.__update_cart_types, self.__handle_failure
        )

    def __update_cart_types(self, cart_types: List[CartType]):
        self.beginResetModel()
        self.__types = cart_types
        self.endResetModel()

    def __handle_failure(self, error: str):
        self.__logger.error(f"Failed reported back to cart type viewmodel: {error}")

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.__types[index.row()].cart_type

    def rowCount(self, index):
        return len(self.__types)

    def addCartType(self, cart_type: str):
        if not cart_type:
            return

        existing_cart_types = [
            existing_cart_type
            for existing_cart_type in self.__types
            if existing_cart_type.cart_type == cart_type
        ]
        if not existing_cart_types:
            self.__cart_type_service.add(
                cart_type, self.__handle_cart_type_action, self.__handle_failure
            )

    def deleteCartType(self, index: int):
        if index < 0 or index >= len(self.__types):
            return

        cart_type = self.__types[index]

        self.__cart_type_service.delete(
            cart_type, self.__handle_none_action, self.__handle_failure
        )

    def __handle_cart_type_action(self, cart_type: CartType):
        self.refresh()

    def __handle_none_action(self):
        self.refresh()
