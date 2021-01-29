import axios, { AxiosResponse } from 'axios'
import { getUrl } from '../../services/UrlService'
import {
  ApiAccess,
  ApiLogin,
  ApiLoginResponse,
  ApiRefresh,
  ApiTenancy
} from '../models/Authentication'
import { generateHeaders } from './Helpers'

export const userLogin = (credentials: ApiLogin): Promise<AxiosResponse<ApiLoginResponse>> => {
  return axios.post<ApiLoginResponse>(getUrl('login', '/api/token/'), credentials)
}

export const getTenancies = (token: string): Promise<AxiosResponse<ApiTenancy[]>> => {
  return axios.get<ApiTenancy[]>(getUrl('login', '/api/token/tenancies/'), generateHeaders(token))
}

export const postRefreshToken = (refreshRequest: ApiRefresh): Promise<AxiosResponse<ApiAccess>> => {
  return axios.post<ApiAccess>(getUrl('login', '/api/token/refresh/'), refreshRequest)
}
