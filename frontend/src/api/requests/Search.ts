/* eslint-disable import/prefer-default-export */
import axios, { AxiosResponse } from 'axios';
import getUrl from 'services/UrlService';
import { CartSearchConditions } from 'api/models/Search';
import { generateRequestConfig } from 'api/requests/Helpers';
import { Paginated } from 'api/models/Pagination';
import { Cart } from 'api/models/Cart';

export const cartSearch = (
  conditions: CartSearchConditions,
): Promise<AxiosResponse<Paginated<Cart>>> => {
  const params = new URLSearchParams();
  params.append('search', conditions.search);
  params.append('page', conditions.page);
  params.append('page_size', conditions.resultsPerPage);
  params.append('ordering', conditions.order);
  return axios.get<Paginated<Cart>>(getUrl('/api/cart/'), generateRequestConfig(params));
};
