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
import Logout from 'pages/Authentication/Logout';
import { AuthenticationContext, AuthenticationStage, AuthenticationStatusProps } from 'components/context/AuthenticationContext';

const mockNavigate = jest.fn();
const mockSetAuthenticationStatus = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('logout page', () => {
  const getComponent = (stage: AuthenticationStage) => {
    const authContextValue : AuthenticationStatusProps = {
      authenticationStatus: {
        stage,
      },
      setAuthenticationStatus: mockSetAuthenticationStatus,
    };
    return mount(
      <AuthenticationContext.Provider value={authContextValue}>
        <Logout />
      </AuthenticationContext.Provider>,
    );
  };

  it('clicking log back in redirects', () => {
    const component = getComponent('Unauthenticated');
    const loginButton = component.find("[data-test='button-login']").first();
    loginButton.simulate('click');
    expect(mockNavigate).toBeCalledWith('/login/');
  });

  it('automatic log out triggers', () => {
    getComponent('Authenticated');
    expect(mockSetAuthenticationStatus).toBeCalledWith({ stage: 'Unauthenticated' });
  });
});
