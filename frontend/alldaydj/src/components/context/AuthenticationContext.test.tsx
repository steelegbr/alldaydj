import React from 'react';
import { mount } from 'enzyme';
import AuthenticationProvider from './AuthenticationContext';
import { refreshAccessToken, getAuthenticationStatusFromLocalStorage } from '../../services/AuthenticationService';
import Dummy from '../test/Dummy';
import { getLogger } from '../../services/LoggingService';

jest.mock('../../services/AuthenticationService');
jest.mock('../../services/LoggingService');
jest.useFakeTimers();

describe('authentication context', () => {
  const mountComponent = () => mount(
    <AuthenticationProvider>
      <Dummy />
    </AuthenticationProvider>,
  );

  it('refresh needed triggers an API call', () => {
    getAuthenticationStatusFromLocalStorage.mockReturnValue({
      stage: 'AccessTokenRefreshNeeded',
      refreshToken: 'refreshTokenValue',
    });

    mountComponent();

    expect(refreshAccessToken).toBeCalledWith('refreshTokenValue', expect.any(Function));
  });

  //   it('status change noticed', () => {
  //     const mockLogger = jest.fn();

  //     getAuthenticationStatusFromLocalStorage.mockReturnValue({
  //       stage: 'Authenticated',
  //     });

  //     getLogger.mockReturnValue(mockLogger);

  //     mountComponent();

  //     getAuthenticationStatusFromLocalStorage.mockReturnValue({
  //       stage: 'AccessTokenRefreshNeeded',
  //     });

  //     jest.runAllTimers();

//     expect(mockLogger).toBeCalledWith({});
//   });
});
