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
  const log = getLogger();

  log.info('Attempting to get authentication status from local storage.');

  const authenticationStatus: AuthenticationStatus = {
    stage: 'Unauthenticated',
  };

  if (refreshToken) {
    const decodedRefreshToken = jwtDecode<JwtToken>(refreshToken);
    const expiry = calculateExpiry(decodedRefreshToken);
    if (expiry > new Date()) {
      log.info(`Valid refresh token expires ${expiry}`);
      authenticationStatus.stage = 'AccessTokenRefreshNeeded';
      authenticationStatus.refreshToken = refreshToken;
      authenticationStatus.refreshTokenExpiry = expiry;
    }

    if (accessToken) {
      const decodedAccessToken = jwtDecode<JwtToken>(accessToken);
      const accessExpiry = calculateExpiry(decodedAccessToken);
      if (accessExpiry > new Date()) {
        log.info(`Valid access token expires ${accessExpiry}`);
        authenticationStatus.stage = 'Authenticated';
        authenticationStatus.accessToken = accessToken;
        authenticationStatus.accessTokenExpiry = accessExpiry;
      }
    }
  }

  log.info(`Current authentication stage is ${authenticationStatus.stage}.`);
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
  const log = getLogger();
  postRefreshToken({ refresh: refreshToken }).then(
    (response) => {
      log.info('Access token refreshed.');
      localStorage.setItem('accessToken', response.data.access);
      setAuthenticationStatus(loginUser(refreshToken, response.data.access));
    },
    (error) => {
      log.error(`Access token refresh failed: ${error}`);
      setAuthenticationStatus({
        stage: 'Unauthenticated',
      });
    },
  );
};
