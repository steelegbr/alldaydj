from models.core.settings import Settings
from models.dto.api import ApiSettings
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkReply
from services.api import ApiService
from tests.services.qt import MockSignal, MockQtHttpResponse
from unittest.mock import MagicMock


def test_api_settings_success(monkeypatch):
    # Arrange
    # Mock out the finished signal

    mock_signal = MockSignal()
    monkeypatch.setattr("services.api.QNetworkAccessManager.finished", mock_signal)

    # Mock out the settings service

    class MockSettingsService:
        def get(self) -> Settings:
            return Settings(base_url="https://example.org")

    api_service = ApiService(settings_service=MockSettingsService())

    # Override the get call

    mock_http_get = MagicMock()
    monkeypatch.setattr("services.api.QNetworkAccessManager.get", mock_http_get)

    # Setup out responces

    mock_success = MagicMock()
    mock_failure = MagicMock()
    mock_response = MockQtHttpResponse(
        response='{"auth_audience":"AUD123", "auth_domain":"auth.example.org", "auth_client_id":"CLIENT123"}'
    )

    # Act
    # Simulate a call, then a callback

    api_service.get_api_settings(mock_success, mock_failure)
    mock_signal.connect_callbacks[0](mock_response)

    # Assert
    # Check a request attempt was made

    mock_http_get.assert_called_once()
    network_request = mock_http_get.call_args[0][0]
    assert network_request.url() == QUrl("https://example.org/api/settings")

    mock_success.assert_called_once_with(
        ApiSettings(
            auth_audience="AUD123",
            auth_domain="auth.example.org",
            auth_client_id="CLIENT123",
        )
    )
    mock_failure.assert_not_called()


def test_api_settings_error(monkeypatch):
    # Arrange
    # Mock out the finished signal

    mock_signal = MockSignal()
    monkeypatch.setattr("services.api.QNetworkAccessManager.finished", mock_signal)

    # Mock out the settings service

    class MockSettingsService:
        def get(self) -> Settings:
            return Settings(base_url="https://example.org")

    api_service = ApiService(settings_service=MockSettingsService())

    # Override the get call

    mock_http_get = MagicMock()
    monkeypatch.setattr("services.api.QNetworkAccessManager.get", mock_http_get)

    # Setup out responces

    mock_success = MagicMock()
    mock_failure = MagicMock()
    mock_response = MockQtHttpResponse(
        error=QNetworkReply.NetworkError.ContentNotFoundError,
        response='{"error": "BAD REQUEST"}',
    )

    # Act
    # Simulate a call, then a callback

    api_service.get_api_settings(mock_success, mock_failure)
    mock_signal.connect_callbacks[0](mock_response)

    # Assert
    # Check a request attempt was made

    mock_http_get.assert_called_once()
    network_request = mock_http_get.call_args[0][0]
    assert network_request.url() == QUrl("https://example.org/api/settings")

    mock_success.assert_not_called()
    mock_failure.assert_called_once_with(
        QNetworkReply.NetworkError.ContentNotFoundError, '{"error": "BAD REQUEST"}'
    )
