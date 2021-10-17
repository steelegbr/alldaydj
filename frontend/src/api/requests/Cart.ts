/* eslint-disable import/prefer-default-export */

import axios from 'axios';
import getUrl from 'services/UrlService';
import { generateRequestConfig } from 'api/requests/Helpers';
import { Cart, CartAudio } from 'api/models/Cart';

export const getCartDetails = (cartId: string, token: string) => axios.get<Cart>(getUrl(`/api/cart/${cartId}/`), generateRequestConfig(token));

export const getCartAudio = (cartId: string, token: string) => axios.get<CartAudio>(getUrl(`/api/audio/${cartId}/`), generateRequestConfig(token));
