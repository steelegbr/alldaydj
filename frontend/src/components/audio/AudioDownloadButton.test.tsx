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
import AudioDownloadButton, { DownloadType } from 'components/audio/AudioDownloadButton';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';
import mockAxios from 'jest-mock-axios';
import { getLogger } from 'services/LoggingService';
import { Logger } from 'loglevel';

const mockLogger = getLogger as jest.Mock<Logger>;
const mockInfo = jest.fn();
const mockError = jest.fn();
const mockDebug = jest.fn();
mockLogger.mockImplementation(() => ({
  info: mockInfo,
  error: mockError,
  debug: mockDebug,
}));

jest.mock('services/LoggingService');

const renderButton = (downloadType: DownloadType) => {
  const contextValue : AuthenticationStatusProps = {
    authenticationStatus: {
      stage: 'Authenticated',
      accessToken: 'TOKEN123',
    },
    setAuthenticationStatus: () => {},
  };
  return mount(
    <AuthenticationContext.Provider value={contextValue}>
      <AudioDownloadButton cartId="UUID123" downloadType={downloadType} label="CART123" />
    </AuthenticationContext.Provider>,
  );
};

describe('audio download button rendering', () => {
  it('render compressed', () => {
    const button = renderButton('Compressed');
    expect(button).toMatchSnapshot();
  });
  it('render compressed', () => {
    const button = renderButton('Linear');
    expect(button).toMatchSnapshot();
  });
});

describe('audio download', () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  it('download happy path', async () => {
    const mockResponse = Promise.resolve({ status: 200, data: { audio: 'http://example.org/UUID123.wav' } });
    mockAxios.get.mockReturnValue(mockResponse);

    const component = renderButton('Linear');
    const button = component.find("button[data-test='button-download-linear']").first();
    button.simulate('click');

    await new Promise((r) => setTimeout(r, 2000));

    expect(mockAxios.get).toBeCalledWith('/api/audio/UUID123/', { headers: { Authorization: 'Bearer TOKEN123' } });
    expect(mockInfo).toBeCalledWith('Attempting to get audio info for cart ID UUID123');
    expect(mockInfo).toBeCalledWith('Successfully obtained cart audio info.');
    expect(mockInfo).toBeCalledWith('Triggered download from http://example.org/UUID123.wav for CART123.wav');
  });

  it('download unhappy path', async () => {
    const mockResponse = Promise.resolve({ status: 404 });
    mockAxios.get.mockReturnValue(mockResponse);

    const component = renderButton('Compressed');
    const button = component.find("button[data-test='button-download-compressed']").first();
    button.simulate('click');

    await new Promise((r) => setTimeout(r, 2000));
    component.update();

    expect(mockAxios.get).toBeCalledWith('/api/audio/UUID123/', { headers: { Authorization: 'Bearer TOKEN123' } });
    expect(mockError).toBeCalledWith('Got a strange HTTP response (404) getting cart audio info.');

    const errorPopup = component.find("[data-test='download-error']").last();
    expect(errorPopup.getDOMNode()).toHaveTextContent('Failed to download the cart audio.');

    expect(component).toMatchSnapshot();
  });
});
