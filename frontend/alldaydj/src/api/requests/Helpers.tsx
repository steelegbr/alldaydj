import { AxiosRequestConfig } from 'axios'

export const generateHeaders = (token: string): AxiosRequestConfig => {
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }
}
