from freezegun import freeze_time
from models.dto.api import ApiSettings
from pathlib import Path
from services.authentication import (
    ApiService,
    AuthenticationService,
    AuthenticationServiceState,
)
from tests.services.logging import mock_logger
from tests.services.qt import MockSignal, MockQtHttpResponse
from unittest.mock import MagicMock

import pytest


@pytest.mark.parametrize(
    "state",
    [
        AuthenticationServiceState.Authenticated,
        AuthenticationServiceState.AwaitingUserAuth,
        AuthenticationServiceState.AuthUrl,
        AuthenticationServiceState.DeviceCode,
        AuthenticationServiceState.RefreshingToken,
        AuthenticationServiceState.TimedOut,
    ],
)
def test_authentication_short_circuit(state: AuthenticationServiceState, mock_logger):
    # Arrange

    authentication_service = AuthenticationService(logger=mock_logger, state=state)

    # Act

    authentication_service.authenticate()

    # Assert

    mock_logger.warning.assert_called_once_with(
        "Can't attempt authentication in current state", state=state
    )


@pytest.mark.parametrize(
    "starting_state",
    [
        AuthenticationServiceState.Unauthenticated,
        AuthenticationServiceState.Error,
    ],
)
def test_happy_path(monkeypatch, starting_state):
    # Arrange
    # Signals

    mock_signal = MockSignal()
    monkeypatch.setattr(
        "services.authentication.QNetworkAccessManager.finished", mock_signal
    )

    # API service

    mock_api = MagicMock()
    monkeypatch.setattr("services.authentication.ApiService.get_api_settings", mock_api)

    # Token validation

    mock_token_validation = MagicMock()
    mock_token_validation.return_value = True
    monkeypatch.setattr(
        "services.authentication.AuthenticationService.is_token_still_valid",
        mock_token_validation,
    )

    # HTTP responses

    http_responses = [
        MockQtHttpResponse(
            '{"device_code": "DEVICE123", "user_code": "USER54321", "verification_uri": "http://example.org/verify", "verification_uri_complete": "http://example.org/verify?device_code=DEVICE123", "expires_in": 500, "interval": 1}'
        ),
        # MockQtHttpResponse('{"error": "authorization_pending", "error_description": "Still waiting on the user..."}', QNetworkReply.NetworkError.ContentAccessDenied)
        MockQtHttpResponse(
            '{"access_token": "TOKEN123", "refresh_token": "REFRESH123", "token_type": "Bearer", "expires_in": 500}'
        ),
    ]

    def run_side_effects(*args, **kwargs):
        mock_signal.connect_callbacks[-1](http_responses.pop(0))

    mock_http_get = MagicMock(side_effect=run_side_effects)
    mock_http_post = MagicMock(side_effect=run_side_effects)

    monkeypatch.setattr(
        "services.authentication.QNetworkAccessManager.get", mock_http_get
    )
    monkeypatch.setattr(
        "services.authentication.QNetworkAccessManager.post", mock_http_post
    )

    # State changes

    state_history = []
    expected_state_history = [
        AuthenticationServiceState.AuthUrl,
        AuthenticationServiceState.DeviceCode,
        AuthenticationServiceState.AwaitingUserAuth,
        AuthenticationServiceState.Authenticated,
    ]

    def state_change_callback(state: AuthenticationServiceState):
        state_history.append(state)

    # The service itself

    authentication_service = AuthenticationService(
        state=starting_state, api_service=ApiService()
    )
    authentication_service.register_callback(state_change_callback)

    # Act
    # We also have to simulate the API service callback

    authentication_service.authenticate()
    mock_api.call_args[0][0](
        ApiSettings(
            auth_audience="AUD123",
            auth_domain="auth.example.org",
            auth_client_id="CLIENT123",
        )
    )

    # Assert

    assert state_history == expected_state_history
    assert mock_http_post.call_count == 2
    assert mock_http_get.call_count == 0
    assert (
        authentication_service.get_state() == AuthenticationServiceState.Authenticated
    )
    assert authentication_service.get_token() == "TOKEN123"


def test_token_invalid():
    # Arrange

    token_filename = Path(__file__).parent / "access_token.json"
    with open(token_filename) as token_handle:
        token = token_handle.read()

    expected = False

    # Act

    actual = AuthenticationService().is_token_still_valid(token)

    # Assert

    assert actual == expected


@freeze_time("2024-12-17")
def test_token_valid():
    # Arrange

    token_filename = Path(__file__).parent / "access_token.json"
    with open(token_filename) as token_handle:
        token = token_handle.read()

    expected = True

    # Act

    actual = AuthenticationService().is_token_still_valid(token)

    # Assert

    assert actual == expected


def test_refresh_token(monkeypatch):
    # Arrange
    # Signals

    mock_signal = MockSignal()
    monkeypatch.setattr(
        "services.authentication.QNetworkAccessManager.finished", mock_signal
    )

    # HTTP responses

    http_responses = [
        MockQtHttpResponse(
            '{"access_token": "ACCESS123", "id_token": "ID123", "scope": "openid profile offline_access", "expires_in": 500, "token_type": "Bearer"}'
        )
    ]

    def run_side_effects(*args, **kwargs):
        mock_signal.connect_callbacks[-1](http_responses.pop(0))

    mock_http_post = MagicMock(side_effect=run_side_effects)
    monkeypatch.setattr(
        "services.authentication.QNetworkAccessManager.post", mock_http_post
    )

    # Token validation

    mock_token_validation = MagicMock()
    mock_token_validation.return_value = True
    monkeypatch.setattr(
        "services.authentication.AuthenticationService.is_token_still_valid",
        mock_token_validation,
    )

    # Service itself

    authentication_service = AuthenticationService()
    authentication_service.set_api_settings(
        ApiSettings(
            auth_audience="AUD123",
            auth_domain="auth.example.org",
            auth_client_id="CLIENT123",
        )
    )
    expected = "ACCESS123"

    # Act

    authentication_service.do_refresh_token("REFRESH123")
    actual = authentication_service.get_token()

    # Assert

    assert actual == expected
    mock_http_post.assert_called_once()
