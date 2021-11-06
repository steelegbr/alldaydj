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

import axios, { AxiosRequestConfig } from 'axios';
import getUrl from 'services/UrlService';
import { generateRequestConfig } from 'api/requests/Helpers';
import {
  AudioUploadJob,
  Cart, CartAudio, CartType, Sequencer, SequencerNext, Tag,
} from 'api/models/Cart';
import getAllPages from 'api/requests/Pagination';
import { CartSearchResult } from 'api/models/Search';

export const getCartDetails = (cartId: string) => axios.get<Cart>(getUrl(`/api/cart/${cartId}/`), generateRequestConfig());

export const getCartAudio = (cartId: string) => axios.get<CartAudio>(getUrl(`/api/audio/${cartId}/`), generateRequestConfig());

export const getCartTypes = () => getAllPages<CartType>(getUrl('/api/type/'));

export const getTags = () => getAllPages<Tag>(getUrl('/api/tag/'));

export const createCart = (cart: Cart) => axios.post<Cart>(getUrl('/api/cart/'), cart, generateRequestConfig());

export const updateCart = (cart: Cart) => axios.put<Cart>(getUrl(`/api/cart/${cart.id}/`), cart, generateRequestConfig());

export const updatePartialCart = (cart: Partial<Cart>) => axios.patch<Cart>(getUrl(`/api/cart/${cart.id}/`), cart, generateRequestConfig());

export const deleteCart = (cart: Cart | CartSearchResult) => axios.delete<Cart>(getUrl(`/api/cart/${cart.id}/`), generateRequestConfig());

export const getUploadJobProgress = (jobId: string) => axios.get<AudioUploadJob>(getUrl(`/api/job/${jobId}/`), generateRequestConfig());

export const getSequencers = () => getAllPages<Sequencer>(getUrl('/api/sequencer/'));

export const getNextCartId = (sequencer: Sequencer) => axios.get<SequencerNext>(getUrl(`/api/sequencer/${sequencer.id}/generate_next/`), generateRequestConfig());

export const uploadAudio = (
  cart: Cart, file: File, progressCallback: (event: ProgressEvent) => void,
) => {
  const baseConfig = generateRequestConfig();
  const config: AxiosRequestConfig = {
    ...baseConfig,
    onUploadProgress: progressCallback,
    headers: {
      ...baseConfig.headers,
      'Content-Type': 'multipart/form-data',
    },
  };

  const data = new FormData();
  data.append('file', file);

  return axios.post<AudioUploadJob>(
    getUrl(`/api/audio/${cart.id}/`),
    data,
    config,
  );
};
