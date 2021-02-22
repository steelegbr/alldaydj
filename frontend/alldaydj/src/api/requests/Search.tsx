/* eslint-disable import/prefer-default-export */
import axios, { AxiosResponse } from 'axios';
import getUrl from '../../services/UrlService';
import { CartSearchResults, CartSearchConditions } from '../models/Search';
import { generateRequestConfig } from './Helpers';

interface CartSearchParams {
    search: string,
    page: number,
    // eslint-disable-next-line camelcase
    page_size: number,
    title?: string,
    artist?: string,
    year?: number
}

const wildcardWrap = (term: string) : string => (term ? `*${term}*` : '*');

export const cartSearch = (
  conditions: CartSearchConditions,
  page: number,
  pageSize: number,
  token: string,
): Promise<AxiosResponse<CartSearchResults>> => {
  const params : CartSearchParams = {
    search: wildcardWrap(conditions.search),
    page,
    page_size: pageSize,
  };

  if (conditions.advanced === 'true') {
    params.title = wildcardWrap(conditions.title);
    params.artist = wildcardWrap(conditions.artist);
  }

  return axios.get<CartSearchResults>(getUrl('/api/cart/search/'), generateRequestConfig(token, params));
};
