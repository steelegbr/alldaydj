from services.logging import LoggingService
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_logger():
    logger = LoggingService().get_logger("TEST")
    logger.warning = MagicMock()
    logger.info = MagicMock()
    logger.debug = MagicMock()
    return logger
