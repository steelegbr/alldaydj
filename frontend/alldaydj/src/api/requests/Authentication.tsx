import axios from 'axios';
import { getUrl } from '../../services/UrlService';
import { ApiLogin, ApiLoginResponse } from '../models/Authentication';

export const userLogin = (credentials: ApiLogin) => {
    return axios.post<ApiLoginResponse>(
        getUrl("login", "/api/token/"),
        credentials
    );
}