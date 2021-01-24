import { AuthenticationStatus, AuthenticationStatusProps } from "../components/context/AuthenticationContext";
import jwt_decode from "jwt-decode";
import { getLogger } from "./LoggingService";

interface JwtToken {
    exp: number
}

const calculateExpiry = (token: JwtToken) => {
    return new Date(token.exp * 1000);
}

export const getAuthenticationStatusFromLocalStorage = (): AuthenticationStatus => {
    const refreshToken = localStorage.getItem('refreshToken');
    const accessToken = localStorage.getItem('accessToken');
    let log = getLogger();

    log.info("Attempting to get authentication status from local storage.")

    let authenticationStatus : AuthenticationStatus = {
        stage: "Unauthenticated"
    };
    
    if (refreshToken) {
        const decodedRefreshToken = jwt_decode<JwtToken>(refreshToken);
        const expiry = calculateExpiry(decodedRefreshToken);
        if (expiry > new Date()) {
            log.info(`Valid refresh token expires ${expiry}`);
            authenticationStatus.stage = "AccessTokenRefreshNeeded";
            authenticationStatus.refreshToken = refreshToken;
            authenticationStatus.refreshTokenExpiry = expiry;
        }

        if (accessToken) {
            const decodedAccessToken = jwt_decode<JwtToken>(accessToken);
            const accessExpiry = calculateExpiry(decodedAccessToken);
            if (expiry > new Date()) {
                log.info(`Valid access token expires ${accessExpiry}`);
                authenticationStatus.stage = "Authenticated";
                authenticationStatus.accessToken = accessToken;
                authenticationStatus.accessTokenExpiry = accessExpiry;
            }
        }

    }


    log.info(`Current authentication stage is ${authenticationStatus.stage}.`)
    return authenticationStatus;
}

export const isAuthenticated = (props: AuthenticationStatusProps | undefined) => {
    const authenticationStage = props?.authenticationStatus.stage;
    return (
        authenticationStage === "Authenticated" || 
        authenticationStage === "RefreshingAccessToken" || 
        authenticationStage === "AccessTokenRefreshNeeded"
    );
}

export const loginUser = (refreshToken: string, accessToken: string) => {

    const decodedRefreshToken = jwt_decode<JwtToken>(refreshToken);
    const decodedAccessToken = jwt_decode<JwtToken>(accessToken);
    const refreshExpiry = calculateExpiry(decodedRefreshToken);
    const accessExpiry = calculateExpiry(decodedAccessToken);

    const authenticationStatus : AuthenticationStatus = {
        stage: "Authenticated",
        refreshToken: refreshToken,
        refreshTokenExpiry: refreshExpiry,
        accessToken: accessToken,
        accessTokenExpiry: accessExpiry
    };

    localStorage.setItem('refreshToken', refreshToken);
    localStorage.setItem('accessToken', accessToken);

    return authenticationStatus;
    
}