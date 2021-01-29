import {
  AuthenticationStatus,
  AuthenticationStatusProps,
} from "../components/context/AuthenticationContext";
import jwtDecode from "jwt-decode";
import { getLogger } from "./LoggingService";

interface JwtToken {
  exp: number;
}

const calculateExpiry = (token: JwtToken) => {
  return new Date(token.exp * 1000);
};

export const getAuthenticationStatusFromLocalStorage = (): AuthenticationStatus => {
  const refreshToken = localStorage.getItem("refreshToken");
  const accessToken = localStorage.getItem("accessToken");
  const tenant = localStorage.getItem("tenant") || undefined;
  const log = getLogger();

  log.info("Attempting to get authentication status from local storage.");

  const authenticationStatus: AuthenticationStatus = {
    stage: "Unauthenticated",
    tenant: tenant,
  };

  if (refreshToken) {
    const decodedRefreshToken = jwtDecode<JwtToken>(refreshToken);
    const expiry = calculateExpiry(decodedRefreshToken);
    if (expiry > new Date()) {
      log.info(`Valid refresh token expires ${expiry}`);
      authenticationStatus.stage = "AccessTokenRefreshNeeded";
      authenticationStatus.refreshToken = refreshToken;
      authenticationStatus.refreshTokenExpiry = expiry;
    }

    if (accessToken) {
      const decodedAccessToken = jwtDecode<JwtToken>(accessToken);
      const accessExpiry = calculateExpiry(decodedAccessToken);
      if (expiry > new Date()) {
        log.info(`Valid access token expires ${accessExpiry}`);
        authenticationStatus.stage = "Authenticated";
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
  requireTenant = false,
): boolean => {
  const authenticationStage = props?.authenticationStatus.stage;
  const tenant = props?.authenticationStatus.tenant;
  const authenticated =
    authenticationStage === "Authenticated" ||
    authenticationStage === "RefreshingAccessToken" ||
    authenticationStage === "AccessTokenRefreshNeeded";
  return requireTenant ? !!(authenticated && tenant) : authenticated;
};

export const loginUser = (refreshToken: string, accessToken: string): AuthenticationStatus => {
  const decodedRefreshToken = jwtDecode<JwtToken>(refreshToken);
  const decodedAccessToken = jwtDecode<JwtToken>(accessToken);
  const refreshExpiry = calculateExpiry(decodedRefreshToken);
  const accessExpiry = calculateExpiry(decodedAccessToken);

  const authenticationStatus: AuthenticationStatus = {
    stage: "Authenticated",
    refreshToken: refreshToken,
    refreshTokenExpiry: refreshExpiry,
    accessToken: accessToken,
    accessTokenExpiry: accessExpiry,
  };

  localStorage.setItem("refreshToken", refreshToken);
  localStorage.setItem("accessToken", accessToken);

  return authenticationStatus;
};

export const logOut = (): AuthenticationStatus => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("tenant");

  const status: AuthenticationStatus = {
    stage: "Unauthenticated",
  };
  return status;
};

export const setTenant = (
  tenant: string,
  authenticationStatus: AuthenticationStatus,
): AuthenticationStatus => {
  localStorage.setItem("tenant", tenant);
  return {
    ...authenticationStatus,
    tenant: tenant,
  };
};
