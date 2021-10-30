/**
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

/* eslint-disable import/prefer-default-export */

import axios from 'axios';
import getUrl from 'services/UrlService';
import { generateRequestConfig } from 'api/requests/Helpers';
import {
  Cart, CartAudio, CartType, Tag,
} from 'api/models/Cart';
import getAllPages from 'api/requests/Pagination';

export const getCartDetails = (cartId: String) => axios.get<Cart>(getUrl(`/api/cart/${cartId}/`), generateRequestConfig());

export const getCartAudio = (cartId: string) => axios.get<CartAudio>(getUrl(`/api/audio/${cartId}/`), generateRequestConfig());

export const getCartTypes = () => getAllPages<CartType>(getUrl('/api/type/'));

export const getTags = () => getAllPages<Tag>(getUrl('/api/tag/'));
