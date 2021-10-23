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
import getAllPages from 'api/requests/Pagination';
import { AxiosResponse } from 'axios';
import mockAxios from 'jest-mock-axios';

describe('pagination', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('happy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<number>>>[] = [
      {
        status: 200,
        data: {
          count: 4,
          next: 'http://example.org/?page=2',
          results: [1, 2],
        },
      },
      {
        status: 200,
        data: {
          count: 4,
          results: [3, 4],
        },
      },
    ];

    const expectedResults = [1, 2, 3, 4];
    const expectedToken = { headers: { Authorization: 'Bearer TOKEN123' } };

    mockAxios.get
      .mockResolvedValueOnce(responses[0])
      .mockResolvedValueOnce(responses[1]);

    const actualResults = await getAllPages('http://example.org/', 'TOKEN123');
    expect(actualResults).toEqual(expectedResults);
    expect(mockAxios.get).toBeCalledTimes(2);
    expect(mockAxios.get).toBeCalledWith('http://example.org/', expectedToken);
    expect(mockAxios.get).toBeCalledWith('http://example.org/?page=2', expectedToken);
  });

  it('unhappy path', async () => {
    const responses: Partial<AxiosResponse<Paginated<number>>>[] = [
      {
        status: 200,
        data: {
          count: 4,
          next: 'http://example.org/?page=2',
          results: [1, 2],
        },
      },
      {
        status: 500,
      },
    ];

    const expectedToken = { headers: { Authorization: 'Bearer TOKEN123' } };

    mockAxios.get
      .mockResolvedValueOnce(responses[0])
      .mockResolvedValueOnce(responses[1]);

    await getAllPages('http://example.org/', 'TOKEN123').catch((error) => expect(error).toBeTruthy());

    expect(mockAxios.get).toBeCalledTimes(2);
    expect(mockAxios.get).toBeCalledWith('http://example.org/', expectedToken);
    expect(mockAxios.get).toBeCalledWith('http://example.org/?page=2', expectedToken);
  });
});
