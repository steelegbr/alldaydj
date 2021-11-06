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

import { cartSearchContextFromQueryString, paramsToSearchConditions } from 'services/SearchService';

describe('cart search service', () => {
  it('querystring params to search conditions empty', () => {
    const converted = paramsToSearchConditions(new URLSearchParams());
    expect(converted).toStrictEqual({
      page: '1',
      resultsPerPage: '10',
      search: '',
      order: 'label',
    });
  });

  it('querystring params to search conditions valid', () => {
    const params : Record<string, string> = {
      page: '5',
      resultsPerPage: '7',
      search: 'something',
      order: 'label',
    };
    const converted = cartSearchContextFromQueryString(new URLSearchParams(params));
    expect(converted).toStrictEqual(
      {
        conditions: {
          page: '5',
          resultsPerPage: '7',
          search: 'something',
          order: 'label',
        },
        status: 'ReadyToSearch',
      },
    );
  });
});
