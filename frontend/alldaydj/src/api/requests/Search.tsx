/* eslint-disable import/prefer-default-export */
import axios, { AxiosResponse } from 'axios';
import getUrl from '../../services/UrlService';
import { CartSearchResults, CartSearchConditions } from '../models/Search';
import { generateRequestConfig } from './Helpers';

const wildcardWrap = (term: string) : string => (term ? `*${term}*` : '*');

export const cartSearch = (
  conditions: CartSearchConditions,
  page: number,
  pageSize: number,
  token: string,
): Promise<AxiosResponse<CartSearchResults>> => {
  const params = new URLSearchParams();
  params.append('search', wildcardWrap(conditions.search));
  params.append('page', `${page}`);
  params.append('page_size', `${pageSize}`);

  if (conditions.advanced === 'true') {
    params.append('search', `title:${wildcardWrap(conditions.title)}`);
    params.append('search', `artist:${wildcardWrap(conditions.artist)}`);
  }

  return axios.get<CartSearchResults>(getUrl('/api/cart/search/'), generateRequestConfig(token, params));
};
