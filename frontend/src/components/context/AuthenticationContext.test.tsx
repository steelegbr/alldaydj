/**
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

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
*/

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
