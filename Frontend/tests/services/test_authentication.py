from services.authentication import AuthenticationService, AuthenticationServiceState
from tests.services.logging import mock_logger

import pytest


@pytest.mark.parametrize(
    "state",
    [
        (AuthenticationServiceState.Authenticated,),
        (AuthenticationServiceState.AwaitingUserAuth),
        (AuthenticationServiceState.AuthUrl),
        (AuthenticationServiceState.DeviceCode),
        (AuthenticationServiceState.RefreshingToken),
        (AuthenticationServiceState.TimedOut),
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
