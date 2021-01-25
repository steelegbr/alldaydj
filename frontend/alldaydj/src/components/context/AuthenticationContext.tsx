import React from 'react';
import { getAuthenticationStatusFromLocalStorage } from '../../services/AuthenticationService';

export type AuthenticationStage = 
    | "Unauthenticated"
    | "AccessTokenRefreshNeeded"
    | "RefreshingAccessToken"
    | "Authenticated"

export interface AuthenticationStatus {
    stage: AuthenticationStage,
    accessToken?: string,
    refreshToken?: string,
    accessTokenExpiry?: Date,
    refreshTokenExpiry?: Date,
    tenant?: string
}

export interface AuthenticationStatusProps {
    authenticationStatus: AuthenticationStatus,
    setAuthenticationStatus: React.Dispatch<React.SetStateAction<AuthenticationStatus>>
}

export const AuthenticationContext = React.createContext<undefined | AuthenticationStatusProps>(undefined);

interface AuthenticationProviderProps {
    children: JSX.Element
}

export const AuthenticationProvider = ({ children }: AuthenticationProviderProps) => {
    const [authenticationStatus, setAuthenticationStatus] = React.useState<AuthenticationStatus>(
        getAuthenticationStatusFromLocalStorage()
    );

    return (
        <AuthenticationContext.Provider value={{ authenticationStatus, setAuthenticationStatus }}>
            {children}
        </AuthenticationContext.Provider>
    )

}