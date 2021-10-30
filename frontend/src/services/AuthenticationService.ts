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

import jwtDecode from 'jwt-decode';
import React from 'react';
import {
  AuthenticationStatus,
  AuthenticationStatusProps,
} from 'components/context/AuthenticationContext';
import { postRefreshToken } from 'api/requests/Authentication';
import { getLogger } from './LoggingService';

interface JwtToken {
  exp: number;
}

const calculateExpiry = (token: JwtToken) => new Date(token.exp * 1000);

export const getAuthenticationStatusFromLocalStorage = (): AuthenticationStatus => {
  const refreshToken = localStorage.getItem('refreshToken');
  const accessToken = localStorage.getItem('accessToken');

  getLogger().info('Attempting to get authentication status from local storage.');

  const authenticationStatus: AuthenticationStatus = {
    stage: 'Unauthenticated',
  };

  if (refreshToken) {
    const decodedRefreshToken = jwtDecode<JwtToken>(refreshToken);
    const expiry = calculateExpiry(decodedRefreshToken);
    if (expiry > new Date()) {
      getLogger().info(`Valid refresh token expires ${expiry}`);
      authenticationStatus.stage = 'AccessTokenRefreshNeeded';
      authenticationStatus.refreshToken = refreshToken;
      authenticationStatus.refreshTokenExpiry = expiry;
    }

    if (accessToken) {
      const decodedAccessToken = jwtDecode<JwtToken>(accessToken);
      const accessExpiry = calculateExpiry(decodedAccessToken);
      if (accessExpiry > new Date()) {
        getLogger().info(`Valid access token expires ${accessExpiry}`);
        authenticationStatus.stage = 'Authenticated';
        authenticationStatus.accessToken = accessToken;
        authenticationStatus.accessTokenExpiry = accessExpiry;
      }
    }
  }

  getLogger().info(`Current authentication stage is ${authenticationStatus.stage}.`);
  return authenticationStatus;
};

export const isAuthenticated = (
  props: AuthenticationStatusProps | undefined,
): boolean => {
  const authenticationStage = props?.authenticationStatus.stage;
  return authenticationStage === 'Authenticated'
    || authenticationStage === 'RefreshingAccessToken'
    || authenticationStage === 'AccessTokenRefreshNeeded';
};

export const loginUser = (refreshToken: string, accessToken: string): AuthenticationStatus => {
  const decodedRefreshToken = jwtDecode<JwtToken>(refreshToken);
  const decodedAccessToken = jwtDecode<JwtToken>(accessToken);
  const refreshExpiry = calculateExpiry(decodedRefreshToken);
  const accessExpiry = calculateExpiry(decodedAccessToken);

  const authenticationStatus: AuthenticationStatus = {
    stage: 'Authenticated',
    refreshToken,
    refreshTokenExpiry: refreshExpiry,
    accessToken,
    accessTokenExpiry: accessExpiry,
  };

  localStorage.setItem('refreshToken', refreshToken);
  localStorage.setItem('accessToken', accessToken);

  return authenticationStatus;
};

export const logOut = (): AuthenticationStatus => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');

  const status: AuthenticationStatus = {
    stage: 'Unauthenticated',
  };
  return status;
};

export const refreshAccessToken = (
  refreshToken: string,
  setAuthenticationStatus: React.Dispatch<React.SetStateAction<AuthenticationStatus>>,
): void => {
  postRefreshToken({ refresh: refreshToken }).then(
    (response) => {
      getLogger().info('Access token refreshed.');
      localStorage.setItem('accessToken', response.data.access);
      setAuthenticationStatus(loginUser(refreshToken, response.data.access));
    },
    (error) => {
      getLogger().error(`Access token refresh failed: ${error}`);
      setAuthenticationStatus({
        stage: 'Unauthenticated',
      });
    },
  );
};

export const getTokenFromLocalStorage = (): string => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    return token;
  }
  return '';
};
