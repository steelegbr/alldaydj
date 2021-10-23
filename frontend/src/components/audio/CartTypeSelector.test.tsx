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
import mockAxios from 'jest-mock-axios';
import { CartType } from 'api/models/Cart';
import { AxiosResponse } from 'axios';
import { Paginated } from 'api/models/Pagination';
import { mount } from 'enzyme';
import CartTypeSelector from 'components/audio/CartTypeSelector';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';

const selectedChangedCallback = jest.fn();
const setAuthStatusCallback = jest.fn();

const getSelector = (selectedType: string) => {
  const contextValue : AuthenticationStatusProps = {
    authenticationStatus: {
      stage: 'Authenticated',
      accessToken: 'TOKEN123',
    },
    setAuthenticationStatus: setAuthStatusCallback,
  };
  return mount(
    <AuthenticationContext.Provider value={contextValue}>
      <CartTypeSelector selectedType={selectedType} setSelectedType={selectedChangedCallback} />
    </AuthenticationContext.Provider>,
  );
};

describe('cart type dropdown', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('happy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<CartType>>>[] = [
      {
        status: 200,
        data: {
          count: 2,
          next: '/api/type/?page=2',
          results: [
            {
              id: '1',
              name: 'Type 1',
              colour: '#FFFFFF',
              now_playing: false,
            },
          ],
        },
      },
      {
        status: 200,
        data: {
          count: 2,
          results: [
            {
              id: '2',
              name: 'Type 2',
              colour: '#FFFFFF',
              now_playing: true,
            },
          ],
        },
      },
    ];

    mockAxios.get
      .mockResolvedValueOnce(responses[0])
      .mockResolvedValueOnce(responses[1]);

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    const component = getSelector('Type 2');
    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(component).toMatchSnapshot();
    expect(mockAxios.get).toBeCalledTimes(2);
    expect(mockAxios.get).toBeCalledWith('/api/type/', expectedHeaders);
    expect(mockAxios.get).toBeCalledWith('/api/type/?page=2', expectedHeaders);
    expect(selectedChangedCallback).not.toBeCalled();
    expect(setAuthStatusCallback).not.toBeCalled();
  });

  it('unhappy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<CartType>>>[] = [
      {
        status: 500,
        data: {
          count: 2,
          next: '/api/type/?page=2',
          results: [
            {
              id: '1',
              name: 'Type 1',
              colour: '#FFFFFF',
              now_playing: false,
            },
          ],
        },
      },
    ];

    mockAxios.get.mockResolvedValueOnce(responses[0]);

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    const component = getSelector('Type 2');
    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(component).toMatchSnapshot();
    expect(mockAxios.get).toBeCalledTimes(1);
    expect(mockAxios.get).toBeCalledWith('/api/type/', expectedHeaders);
    expect(selectedChangedCallback).not.toBeCalled();
    expect(setAuthStatusCallback).not.toBeCalled();
  });
});
