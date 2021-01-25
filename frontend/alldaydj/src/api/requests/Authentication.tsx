import axios from 'axios';
import { getUrl } from '../../services/UrlService';
import { ApiLogin, ApiLoginResponse, ApiTenancy } from '../models/Authentication';
import { generateHeaders } from './Helpers';

export const userLogin = (credentials: ApiLogin) => {
    return axios.post<ApiLoginResponse>(
        getUrl("login", "/api/token/"),
        credentials
    );
}

export const getTenancies = (token: string) => {
    return axios.get<ApiTenancy[]>(
        getUrl("login", "/api/token/tenancies/"),
        generateHeaders(token)
    )
}