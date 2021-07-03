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

import { CartSearchConditions } from 'api/models/Search';
import { CartSearch } from 'components/context/CartSearchContext';

const parseNumber = (raw: string | null, defaultValue = 1): string => {
  const parsedInt = parseInt(raw || '', 10);
  if (Number.isNaN(parsedInt) || parsedInt <= 0) {
    return `${defaultValue}`;
  }
  return `${parsedInt}`;
};

export const paramsToSearchConditions = (query: URLSearchParams) : CartSearchConditions => ({
  search: query.get('search') || '',
  page: parseNumber(query.get('page')),
  resultsPerPage: parseNumber(query.get('resultsPerPage'), 10),
});

export const cartSearchContextFromQueryString = (query: URLSearchParams): CartSearch => ({
  conditions: paramsToSearchConditions(query),
  status: 'ReadyToSearch',
});
