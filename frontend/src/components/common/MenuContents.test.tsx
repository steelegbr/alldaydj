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
import MenuContents from 'components/common/MenuContents';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';

const mockPush = jest.fn();
const mockSetAuthStatus = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
}));

describe('menu contents', () => {
  const mountComponent = () => {
    const contextValue : AuthenticationStatusProps = {
      authenticationStatus: {
        stage: 'Authenticated',
      },
      setAuthenticationStatus: mockSetAuthStatus,
    };
    return mount(
      <AuthenticationContext.Provider value={contextValue}>
        <MenuContents />
      </AuthenticationContext.Provider>,
    );
  };

  it('snapshot', () => {
    const component = mountComponent();
    expect(component).toMatchSnapshot();
  });

  it('log out', () => {
    const component = mountComponent();
    const logoutButton = component.find("[data-test='button-logout']").first();
    logoutButton.simulate('click');
    expect(mockPush).toBeCalledWith('/logout/');
  });

  it('library', () => {
    const component = mountComponent();
    const libraryButton = component.find("[data-test='button-library']").first();
    libraryButton.simulate('click');
    expect(mockPush).toBeCalledWith('/library/');
  });
});
