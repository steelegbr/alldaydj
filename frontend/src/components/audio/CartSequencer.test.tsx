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

import { mount } from 'enzyme';
import React from 'react';
import mockAxios from 'jest-mock-axios';
import CartSequencer from 'components/audio/CartSequencer';
import { getTokenFromLocalStorage } from 'services/AuthenticationService';
import { act } from '@testing-library/react';

const mockCallback = jest.fn();
const mockToken = getTokenFromLocalStorage as jest.Mock;
jest.mock('services/AuthenticationService');

const renderSequencer = () => mount(<CartSequencer callback={mockCallback} />);

describe('happy path', () => {
  it('component renders and cart it is returned', async () => {
    const responseSequencers = Promise.resolve({
      status: 200,
      data: {
        count: 1,
        next: null,
        results: [
          {
            id: 'TESTSEQ',
            name: 'Test Sequencer',
          },
        ],
      },
    });

    const responseCartId = Promise.resolve({
      status: 200,
      data: {
        next: 'TESTCART1',
      },
    });
    mockAxios.get
      .mockResolvedValueOnce(responseSequencers)
      .mockResolvedValueOnce(responseCartId);

    mockToken.mockReturnValue('TOKEN123');

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    const component = renderSequencer();
    await act(async () => {
      await responseSequencers;
    });
    component.update();

    const button = component.find("button[data-test='button-generate']").first();
    button.simulate('click');
    await act(async () => {
      await responseCartId;
    });

    expect(mockCallback).toBeCalledTimes(1);
    expect(mockCallback).toBeCalledWith('TESTCART1');

    expect(mockAxios.get).toBeCalledTimes(2);
    expect(mockAxios.get).toBeCalledWith('/api/sequencer/', expectedHeaders);
    expect(mockAxios.get).toBeCalledWith('/api/sequencer/TESTSEQ/generate_next/', expectedHeaders);
  });
});
