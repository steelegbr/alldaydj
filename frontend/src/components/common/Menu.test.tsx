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
import Menu from 'components/common/Menu';
import { AuthenticationContext, AuthenticationStatusProps } from 'components/context/AuthenticationContext';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const mockSetAuthStatus = jest.fn();
const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

const theme = createTheme();

describe('main menu', () => {
  const mountComponent = () => {
    const contextValue : AuthenticationStatusProps = {
      authenticationStatus: {
        stage: 'Authenticated',
      },
      setAuthenticationStatus: mockSetAuthStatus,
    };
    return mount(
      <AuthenticationContext.Provider value={contextValue}>
        <ThemeProvider theme={theme}>
          <Menu />
        </ThemeProvider>
      </AuthenticationContext.Provider>,
    );
  };

  it('snapshot', () => {
    const component = mountComponent();
    expect(component).toMatchSnapshot();
  });

  it('snapshot menu opened', () => {
    const component = mountComponent();
    const buttonToggleMenu = component.find("[data-test='button-menu-toggle']").first();
    buttonToggleMenu.simulate('click');
    component.update();
    expect(component).toMatchSnapshot();
  });
});
