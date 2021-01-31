/* eslint-disable import/prefer-default-export */
import { AxiosRequestConfig } from 'axios';

export const generateHeaders = (token: string): AxiosRequestConfig => ({
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
