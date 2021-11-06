/* eslint-disable import/prefer-default-export */
import { AxiosRequestConfig } from 'axios';
import { getTokenFromLocalStorage } from 'services/AuthenticationService';

export const generateRequestConfig = (
  params?: object,
): AxiosRequestConfig => {
  const token = getTokenFromLocalStorage();
  const requestConfig : AxiosRequestConfig = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  if (params) {
    requestConfig.params = params;
  }

  return requestConfig;
};
