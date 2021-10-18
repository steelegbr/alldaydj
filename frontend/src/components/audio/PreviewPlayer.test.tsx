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

/**

    Just a quick note on the limitations of this test.
    There's very little audio stuff we can actually play with here.
    The HTML5 Audio component is not sufficiently simulated to fully test this out.

*/

import PreviewPlayer from 'components/audio/PreviewPlayer';
import { PreviewContext, PreviewContextType } from 'components/context/PreviewContext';
import { mount } from 'enzyme';
import React from 'react';
import mockAxios from 'jest-mock-axios';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';
import { act } from '@testing-library/react';

const CART_ID = 'CART123';
const mockSetCartId = jest.fn();
const mockClearCart = jest.fn();
const mockSetAuthenticationStatus = jest.fn();

const loadPlayer = () => {
  const previewContextConfig: PreviewContextType = {
    cartId: CART_ID,
    setCartId: mockSetCartId,
    clearCart: mockClearCart,
  };
  const authContextConfig : AuthenticationStatusProps = {
    authenticationStatus: {
      stage: 'Authenticated',
      accessToken: 'TOKEN123',
    },
    setAuthenticationStatus: mockSetAuthenticationStatus,
  };
  return mount(
    <AuthenticationContext.Provider value={authContextConfig}>
      <PreviewContext.Provider value={previewContextConfig}>
        <PreviewPlayer />
      </PreviewContext.Provider>
    </AuthenticationContext.Provider>,
  );
};

describe('happy path', () => {
  beforeAll(() => {
    jest.resetAllMocks();
  });
  it('loads and unloads', async () => {
    const responseGetCartDetails = Promise.resolve({
      status: 200,
      data: {
        title: 'The Song',
        display_artist: 'The Title',
        cue_audio_start: 0,
        cue_audio_end: 4,
        cue_intro_start: 1,
        cue_intro_end: 2,
        cue_segue: 3,
      },
    });

    const responseGetCartAudio = Promise.resolve({
      status: 200,
      data: {
        audio: 'https://www.example.org/CART123.wav',
        compressed: 'https://www.example.org/CART123.ogg',
        hash_audio: 'HASHWAV',
        hash_compressed: 'HASHOGG',
      },
    });

    mockAxios.get.mockResolvedValueOnce(responseGetCartDetails)
      .mockResolvedValueOnce(responseGetCartAudio);

    const component = loadPlayer();
    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(component).toMatchSnapshot();

    const button = component.find("button[data-test='button-close']").first();
    button.simulate('click');

    expect(mockClearCart).toBeCalled();
    expect(mockSetCartId).not.toBeCalled();
    expect(mockAxios.get).toBeCalledWith('/api/cart/CART123/', { headers: { Authorization: 'Bearer TOKEN123' } });
    expect(mockAxios.get).toBeCalledWith('/api/audio/CART123/', { headers: { Authorization: 'Bearer TOKEN123' } });
  });
});

describe('unhappy path', () => {
  beforeAll(() => {
    jest.resetAllMocks();
  });
  it('fails on first http request', async () => {
    const responseGetCartDetails = Promise.resolve({
      status: 404,
    });

    mockAxios.get.mockResolvedValueOnce(responseGetCartDetails);

    const component = loadPlayer();
    await act(async () => {
      await responseGetCartDetails;
    });
    component.update();

    const errorMessage = component.find("[data-test='preview-error']").last();
    expect(errorMessage.getDOMNode()).toHaveTextContent('Something went wrong trying to preview cart audio. Please try again later.');

    expect(component).toMatchSnapshot();

    expect(mockClearCart).not.toBeCalled();
    expect(mockSetCartId).not.toBeCalled();
    expect(mockAxios.get).toBeCalledWith('/api/cart/CART123/', { headers: { Authorization: 'Bearer TOKEN123' } });
  });

  it('fails on second http request', async () => {
    const responseGetCartDetails = Promise.resolve({
      status: 200,
      data: {
        title: 'The Song',
        display_artist: 'The Title',
        cue_audio_start: 0,
        cue_audio_end: 4,
        cue_intro_start: 1,
        cue_intro_end: 2,
        cue_segue: 3,
      },
    });

    const responseGetCartAudio = Promise.resolve({
      status: 404,
    });

    mockAxios.get.mockResolvedValueOnce(responseGetCartDetails)
      .mockResolvedValueOnce(responseGetCartAudio);

    const component = loadPlayer();
    await act(async () => {
      await responseGetCartDetails;
    });
    component.update();

    const errorMessage = component.find("[data-test='preview-error']").last();
    expect(errorMessage.getDOMNode()).toHaveTextContent('Something went wrong trying to preview cart audio. Please try again later.');

    expect(component).toMatchSnapshot();

    expect(mockClearCart).not.toBeCalled();
    expect(mockSetCartId).not.toBeCalled();
    expect(mockAxios.get).toBeCalledWith('/api/cart/CART123/', { headers: { Authorization: 'Bearer TOKEN123' } });
    expect(mockAxios.get).toBeCalledWith('/api/audio/CART123/', { headers: { Authorization: 'Bearer TOKEN123' } });
  });
});
