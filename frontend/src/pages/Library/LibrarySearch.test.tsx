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

import React from 'react';
import { mount } from 'enzyme';
import { CartSearchConditionFields, CartSearchOrderBy } from 'api/models/Search';
import CartSearchContext, { CartSearchContextType, CartSearchStatus } from 'components/context/CartSearchContext';
import LibrarySearch from 'pages/Library/LibrarySearch';

const mockNavigate = jest.fn();
const mockSetSearch = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('cart library search', () => {
  const getComponent = (
    conditions: Record<CartSearchConditionFields, string>,
    status: CartSearchStatus,
  ) => {
    const contextParams : CartSearchContextType = {
      search: {
        conditions,
        status,
      },
      setSearch: mockSetSearch,
    };
    return mount(
      <CartSearchContext.Provider value={contextParams}>
        <LibrarySearch />
      </CartSearchContext.Provider>,
    );
  };

  it('basic search', () => {
    const component = getComponent(
      {
        page: '1',
        resultsPerPage: '10',
        search: '',
        order: CartSearchOrderBy.Label,
      },
      'NotStarted',
    );

    const searchBox = component.find("[data-test='input-search']").find('input');
    searchBox.simulate('change', { target: { value: 'Test' } });
    component.update();

    const searchButton = component.find("[data-test='button-search']").find('button');
    searchButton.simulate('submit');

    expect(mockSetSearch).toBeCalledTimes(2);
    expect(mockSetSearch).toBeCalledWith({
      conditions: {
        page: '1',
        resultsPerPage: '10',
        search: 'Test',
        order: 'label',
      },
      status: 'NotStarted',
    });
    expect(mockSetSearch).toBeCalledWith({
      conditions: {
        page: '1',
        resultsPerPage: '10',
        search: '',
        order: 'label',
      },
      status: 'ReadyToSearch',
    });
    expect(mockNavigate).toBeCalledWith({
      pathname: '/library/',
      search: '?page=1&resultsPerPage=10&search=&order=label',
    });
  });

  it('search does not trigger when in loading state', () => {
    const component = getComponent(
      {
        page: '1',
        resultsPerPage: '10',
        search: 'Test',
        order: CartSearchOrderBy.Label,
      },
      'Searching',
    );

    component.update();
    jest.clearAllMocks();

    const searchButton = component.find("[data-test='button-search']").find('button');
    searchButton.simulate('submit');

    expect(mockSetSearch).not.toBeCalled();
    expect(mockNavigate).not.toBeCalled();
  });
});
