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
import { getTokenFromLocalStorage } from 'services/AuthenticationService';
import { act } from '@testing-library/react';
import { Cart } from 'api/models/Cart';
import CartDeleteAlert from 'components/audio/CartDeleteAlert';

const mockOnDelete = jest.fn();
const mockOnCancel = jest.fn();
const mockToken = getTokenFromLocalStorage as jest.Mock;
jest.mock('services/AuthenticationService');

const renderAlert = () => {
  const cart: Cart = {
    id: 'ID123',
    label: 'LABEL123',
    title: '',
    display_artist: '',
    cue_audio_start: 0,
    cue_audio_end: 0,
    cue_intro_end: 0,
    cue_segue: 0,
    artists: [],
    sweeper: false,
    year: 2021,
    tags: [],
    type: '',
    fade: false,
  };
  return mount(<CartDeleteAlert cart={cart} onCancel={mockOnCancel} onDelete={mockOnDelete} />);
};

describe('delete cart alert box', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('cancel calls the callback', () => {
    const component = renderAlert();
    expect(component).toMatchSnapshot();

    const button = component.find("button[data-test='alert-button-cancel']").first();
    button.simulate('click');

    expect(mockOnCancel).toBeCalledTimes(1);
    expect(mockOnDelete).not.toBeCalled();
    expect(mockAxios.delete).not.toBeCalled();
    expect(mockToken).not.toBeCalled();
  });

  it('delete happy path', async () => {
    const responseDelete = Promise.resolve({
      status: 204,
      data: {},
    });
    mockAxios.delete.mockResolvedValueOnce(responseDelete);
    mockToken.mockReturnValue('TOKEN123');

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    const component = renderAlert();
    const button = component.find("button[data-test='alert-button-delete']").first();
    button.simulate('click');
    await act(async () => {
      await responseDelete;
    });

    expect(mockOnCancel).not.toBeCalled();
    expect(mockOnDelete).toBeCalledTimes(1);
    expect(mockAxios.delete).toBeCalledWith('/api/cart/ID123/', expectedHeaders);
    expect(mockToken).toBeCalled();
  });

  it('delete unhappy path', async () => {
    const responseDelete = Promise.resolve({
      status: 404,
      data: {},
    });
    mockAxios.delete.mockResolvedValueOnce(responseDelete);
    mockToken.mockReturnValue('TOKEN123');

    const expectedHeaders = { headers: { Authorization: 'Bearer TOKEN123' } };

    const component = renderAlert();
    const button = component.find("button[data-test='alert-button-delete']").first();
    button.simulate('click');
    await act(async () => {
      await responseDelete;
    });

    component.update();
    const errorAlert = component.find("[data-test='error']").last();
    expect(errorAlert.getDOMNode().textContent).toContain('Something went wrong attempting to delete the cart. Please try again later.');

    expect(mockOnCancel).not.toBeCalled();
    expect(mockOnDelete).not.toBeCalled();
    expect(mockAxios.delete).toBeCalledWith('/api/cart/ID123/', expectedHeaders);
    expect(mockToken).toBeCalled();
  });
});
