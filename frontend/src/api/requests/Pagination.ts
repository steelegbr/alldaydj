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

import { Paginated } from 'api/models/Pagination';
import { generateRequestConfig } from 'api/requests/Helpers';
import axios, { AxiosResponse } from 'axios';

export async function getAllPages<Type>(url: string, token: string): Promise<Type[]> {
  let objects: Type[] = [];
  let nextUrl: string | undefined = url;

  /* eslint-disable no-await-in-loop */
  while (nextUrl) {
    const response: AxiosResponse<Paginated<Type>> = await axios.get<Paginated<Type>>(
      nextUrl, generateRequestConfig(token),
    );
    if (response.status === 200) {
      objects = [...objects, ...response.data.results];
      nextUrl = response.data.next;
    } else {
      throw new Error(`Got a strange response code: ${response.status}`);
    }
  }
  /* eslint-enable no-await-in-loop */

  return objects;
}

export default getAllPages;
