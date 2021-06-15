import axios, { AxiosResponse } from 'axios';
import getUrl from '../../services/UrlService';
import {
  ApiAccess,
  ApiLogin,
  ApiLoginResponse,
  ApiRefresh,
  ApiForgottenPassword,
  ApiCheckPasswordResetToken,
  ApiPasswordReset,
} from '../models/Authentication';

export const userLogin = (credentials: ApiLogin): Promise<AxiosResponse<ApiLoginResponse>> => axios.post<ApiLoginResponse>(getUrl('/api/token/'), credentials);

export const postRefreshToken = (refreshRequest: ApiRefresh): Promise<AxiosResponse<ApiAccess>> => axios.post<ApiAccess>(getUrl('/api/token/refresh/'), refreshRequest);

export const forgottenPassword = (forgottenPasswordRequest: ApiForgottenPassword): Promise<AxiosResponse> => axios.post(getUrl('/api/password-reset/'), forgottenPasswordRequest);

export const testPasswordResetToken = (tokenTestRequest: ApiCheckPasswordResetToken): Promise<AxiosResponse> => axios.post(getUrl('/api/password-reset/validate_token/'), tokenTestRequest);

export const passwordReset = (passwordResetRequest: ApiPasswordReset): Promise<AxiosResponse> => axios.post(getUrl('/api/password-reset/confirm/'), passwordResetRequest);
