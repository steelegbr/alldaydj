import React, { useEffect } from 'react';
import {
  getAuthenticationStatusFromLocalStorage,
  refreshAccessToken,
} from '../../services/AuthenticationService';
import { getLogger } from '../../services/LoggingService';

export type AuthenticationStage =
  | 'Unauthenticated'
  | 'AccessTokenRefreshNeeded'
  | 'RefreshingAccessToken'
  | 'Authenticated';

export interface AuthenticationStatus {
  stage: AuthenticationStage;
  accessToken?: string;
  refreshToken?: string;
  accessTokenExpiry?: Date;
  refreshTokenExpiry?: Date;
  tenant?: string;
}

export interface AuthenticationStatusProps {
  authenticationStatus: AuthenticationStatus;
  setAuthenticationStatus: React.Dispatch<React.SetStateAction<AuthenticationStatus>>;
}

export const AuthenticationContext = React.createContext<undefined | AuthenticationStatusProps>(
  undefined,
);

export interface AuthenticationProviderProps {
  children: React.ReactElement;
}

const AuthenticationProvider = ({ children }: AuthenticationProviderProps): React.ReactElement => {
  const [authenticationStatus, setAuthenticationStatus] = React.useState<AuthenticationStatus>(
    getAuthenticationStatusFromLocalStorage(),
  );

  useEffect(() => {
    const interval = setInterval(() => {
      const log = getLogger();
      log.debug('Checking current authentication status.');

      const newAuthStatus = getAuthenticationStatusFromLocalStorage();
      if (newAuthStatus.stage !== authenticationStatus.stage) {
        log.info(`Change of authentication stage to ${newAuthStatus.stage}.`);
        setAuthenticationStatus(newAuthStatus);
      }
    }, Number(process.env.REACT_APP_AUTH_INTERVAL || '5000'));

    return () => clearInterval(interval);
  }, [authenticationStatus.stage]);

  useEffect(() => {
    if (authenticationStatus.stage === 'AccessTokenRefreshNeeded') {
      refreshAccessToken(authenticationStatus.refreshToken || '', setAuthenticationStatus);
    }
  }, [authenticationStatus]);

  return (
    <AuthenticationContext.Provider value={{ authenticationStatus, setAuthenticationStatus }}>
      {children}
    </AuthenticationContext.Provider>
  );
};

export default AuthenticationProvider;
