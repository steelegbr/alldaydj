import React from 'react';
import { mount } from 'enzyme';
import Logout from './Logout';
import { AuthenticationContext, AuthenticationStage, AuthenticationStatusProps } from '../../components/context/AuthenticationContext';

const mockPush = jest.fn();
const mockSetAuthenticationStatus = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
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
    expect(mockPush).toBeCalledWith('/login/');
  });

  it('automatic log out triggers', () => {
    getComponent('Authenticated');
    expect(mockSetAuthenticationStatus).toBeCalledWith({ stage: 'Unauthenticated' });
  });
});
