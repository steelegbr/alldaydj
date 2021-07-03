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

import { act } from '@testing-library/react';
import { postRefreshToken } from 'api/requests/Authentication';
import { AuthenticationStatus } from 'components/context/AuthenticationContext';
import { advanceTo } from 'jest-date-mock';
import {
  getAuthenticationStatusFromLocalStorage, isAuthenticated, loginUser, logOut, refreshAccessToken,
} from 'services/AuthenticationService';

const mockPostRefreshToken = postRefreshToken as jest.Mock;
const INVALID_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZXhwIjoxNTE2MjM5MDIyfQ.E9bQ6QAil4HpH825QC5PtjNGEDQTtMpcj0SO2W8vmag';
const VALID_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZXhwIjoxNjE0NTUzMTgzfQ.OR14KFT2Vkp6j7nKEBK3mSmnXjy9pYvJXht8T41-2Cw';
const VALID_DATE = new Date('2021-02-28T22:59:43.000Z');

jest.mock('api/requests/Authentication');

describe('authentication service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    advanceTo(new Date(2021, 1, 1, 0, 0, 0));
  });

  it.each`
  refreshToken | accessToken | expectedAuthStage
  ${''} | ${''} | ${'Unauthenticated'}
  ${INVALID_TOKEN} | ${''} | ${'Unauthenticated'}
  ${VALID_TOKEN} | ${''} | ${'AccessTokenRefreshNeeded'}
  ${VALID_TOKEN} | ${VALID_TOKEN} | ${'Authenticated'}
  `('token status from local storage', ({
    refreshToken,
    accessToken,
    expectedAuthStage,
  }) => {
    localStorage.setItem('refreshToken', refreshToken);
    localStorage.setItem('accessToken', accessToken);

    const authStatus = getAuthenticationStatusFromLocalStorage();

    expect(authStatus.stage).toStrictEqual(expectedAuthStage);
    expect(localStorage.getItem).toBeCalledTimes(2);
    expect(localStorage.getItem).toBeCalledWith('refreshToken');
    expect(localStorage.getItem).toBeCalledWith('accessToken');
  });

  it.each`
  stage | expectedResponse
  ${'Authenticated'} | ${true}
  ${'Unauthenticated'} | ${false}
  ${'RefreshingAccessToken'} | ${true}
  ${'AccessTokenRefreshNeeded'} | ${true}
  `('is authenticated', ({ stage, expectedResponse }) => {
    const actualResponse = isAuthenticated({
      authenticationStatus: {
        stage,
      },
    });
    expect(actualResponse).toStrictEqual(expectedResponse);
  });

  it('user login', () => {
    const expectedResponse : AuthenticationStatus = {
      stage: 'Authenticated',
      accessToken: VALID_TOKEN,
      accessTokenExpiry: VALID_DATE,
      refreshToken: VALID_TOKEN,
      refreshTokenExpiry: VALID_DATE,
    };

    const actualResponse = loginUser(VALID_TOKEN, VALID_TOKEN);

    expect(actualResponse).toStrictEqual(expectedResponse);
    expect(localStorage.setItem).toBeCalledTimes(2);
    expect(localStorage.setItem).toBeCalledWith('refreshToken', VALID_TOKEN);
    expect(localStorage.setItem).toBeCalledWith('accessToken', VALID_TOKEN);
  });

  it('log out', () => {
    logOut();
    expect(localStorage.removeItem).toBeCalledTimes(2);
    expect(localStorage.removeItem).toBeCalledWith('refreshToken');
    expect(localStorage.removeItem).toBeCalledWith('accessToken');
  });

  it('refresh access token success', async () => {
    const refreshSuccess = Promise.resolve({
      data: {
        access: VALID_TOKEN,
      },
    });
    mockPostRefreshToken.mockReturnValue(refreshSuccess);
    const mockSetAuthStatus = jest.fn();

    refreshAccessToken(VALID_TOKEN, mockSetAuthStatus);
    await act(async () => {
      await mockPostRefreshToken;
    });

    expect(mockPostRefreshToken).toBeCalledTimes(1);
    expect(mockPostRefreshToken).toBeCalledWith({
      refresh: VALID_TOKEN,
    });
    expect(mockSetAuthStatus).toBeCalledTimes(1);
    expect(mockSetAuthStatus).toBeCalledWith({
      stage: 'Authenticated',
      accessToken: VALID_TOKEN,
      accessTokenExpiry: VALID_DATE,
      refreshToken: VALID_TOKEN,
      refreshTokenExpiry: VALID_DATE,
    });
  });

  it('refresh access token failure', async () => {
    const refreshFailure = Promise.reject(new Error('Cannot refresh token'));
    mockPostRefreshToken.mockReturnValue(refreshFailure);
    const mockSetAuthStatus = jest.fn();

    refreshAccessToken(VALID_TOKEN, mockSetAuthStatus);
    await act(async () => {
      await mockPostRefreshToken;
    });

    expect(mockPostRefreshToken).toBeCalledTimes(1);
    expect(mockPostRefreshToken).toBeCalledWith({
      refresh: VALID_TOKEN,
    });
    expect(mockSetAuthStatus).toBeCalledTimes(1);
    expect(mockSetAuthStatus).toBeCalledWith({
      stage: 'Unauthenticated',
    });
  });
});
