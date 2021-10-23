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
import { AxiosResponse } from 'axios';
import mockAxios from 'jest-mock-axios';
import TagChips from 'components/audio/TagChips';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';
import { mount } from 'enzyme';
import { Paginated } from 'api/models/Pagination';
import { Tag } from 'api/models/Cart';

const chipsChangedCallback = jest.fn();
const setAuthStatusCallback = jest.fn();

const getChips = (selectedTags: string[]) => {
  const contextValue : AuthenticationStatusProps = {
    authenticationStatus: {
      stage: 'Authenticated',
      accessToken: 'TOKEN123',
    },
    setAuthenticationStatus: setAuthStatusCallback,
  };
  return mount(
    <AuthenticationContext.Provider value={contextValue}>
      <TagChips selectedTags={selectedTags} setSelectedTags={chipsChangedCallback} />
    </AuthenticationContext.Provider>,
  );
};

describe('tag chips', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('happy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<Tag>>>[] = [
      {
        status: 200,
        data: {
          count: 2,
          next: '/api/tag/?page=2',
          results: [
            {
              id: '1',
              tag: 'Tag 1',
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
              tag: 'Tag 2',
            },
          ],
        },
      },
    ];

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    mockAxios.get
      .mockResolvedValueOnce(responses[0])
      .mockResolvedValueOnce(responses[1]);

    const component = getChips(['Tag 1']);
    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(mockAxios.get).toBeCalledTimes(2);
    expect(mockAxios.get).toBeCalledWith('/api/tag/', expectedHeaders);
    expect(mockAxios.get).toBeCalledWith('/api/tag/?page=2', expectedHeaders);
    expect(chipsChangedCallback).not.toBeCalled();
    expect(setAuthStatusCallback).not.toBeCalled();
  });

  it('unhappy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<Tag>>>[] = [
      {
        status: 500,
        data: {
          count: 2,
          next: '/api/tag/?page=2',
          results: [
            {
              id: '1',
              tag: 'Tag 1',
            },
          ],
        },
      },
    ];

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    mockAxios.get.mockResolvedValueOnce(responses[0]);

    const component = getChips(['Tag 1']);
    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(mockAxios.get).toBeCalledTimes(1);
    expect(mockAxios.get).toBeCalledWith('/api/tag/', expectedHeaders);
    expect(chipsChangedCallback).not.toBeCalled();
    expect(setAuthStatusCallback).not.toBeCalled();
  });
});
