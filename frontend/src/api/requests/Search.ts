/* eslint-disable import/prefer-default-export */
import axios, { AxiosResponse } from 'axios';
import getUrl from 'services/UrlService';
import { CartSearchResults, CartSearchConditions } from 'api/models/Search';
import { generateRequestConfig } from 'api/requests/Helpers';

export const cartSearch = (
  conditions: CartSearchConditions,
  token: string,
): Promise<AxiosResponse<CartSearchResults>> => {
  const params = new URLSearchParams();
  params.append('search', conditions.search);
  params.append('page', conditions.page);
  params.append('page_size', conditions.resultsPerPage);
  return axios.get<CartSearchResults>(getUrl('/api/cart/search/'), generateRequestConfig(token, params));
};
