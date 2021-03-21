import React from 'react';
import { mount } from 'enzyme';
import AuthenticationProvider from 'components/context/AuthenticationContext';
import { refreshAccessToken, getAuthenticationStatusFromLocalStorage } from 'services/AuthenticationService';
import Dummy from 'components/test/Dummy';

const mockGetAuthenticationStatus = getAuthenticationStatusFromLocalStorage as jest.Mock;

jest.mock('services/AuthenticationService');
jest.mock('services/LoggingService');
jest.useFakeTimers();

describe('authentication context', () => {
  const mountComponent = () => mount(
    <AuthenticationProvider>
      <Dummy />
    </AuthenticationProvider>,
  );

  it('refresh needed triggers an API call', () => {
    mockGetAuthenticationStatus.mockReturnValue({
      stage: 'AccessTokenRefreshNeeded',
      refreshToken: 'refreshTokenValue',
    });

    mountComponent();

    expect(refreshAccessToken).toBeCalledWith('refreshTokenValue', expect.any(Function));
  });
});
