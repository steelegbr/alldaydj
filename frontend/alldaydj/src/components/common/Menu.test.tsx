import React from 'react';
import { mount } from 'enzyme';
import Menu from './Menu';
import { AuthenticationContext, AuthenticationStatusProps } from '../context/AuthenticationContext';

const mockSetAuthStatus = jest.fn();

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
        <Menu />
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
