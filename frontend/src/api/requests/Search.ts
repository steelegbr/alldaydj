/* eslint-disable import/prefer-default-export */
import axios, { AxiosResponse } from 'axios';
import getUrl from 'services/UrlService';
import { CartSearchConditions, CartSearchResult } from 'api/models/Search';
import { generateRequestConfig } from 'api/requests/Helpers';
import { Paginated } from 'api/models/Pagination';

export const cartSearch = (
  conditions: CartSearchConditions,
  token: string,
): Promise<AxiosResponse<Paginated<CartSearchResult>>> => {
  const params = new URLSearchParams();
  params.append('search', conditions.search);
  params.append('page', conditions.page);
  params.append('page_size', conditions.resultsPerPage);
  return axios.get<Paginated<CartSearchResult>>(getUrl('/api/cart/search/'), generateRequestConfig(token, params));
};
