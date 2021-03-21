/* eslint-disable import/prefer-default-export */
import { AxiosRequestConfig } from 'axios';

export const generateRequestConfig = (
  token: string,
  params?: object,
): AxiosRequestConfig => {
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
