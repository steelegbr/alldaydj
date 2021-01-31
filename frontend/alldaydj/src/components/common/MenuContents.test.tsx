import React from 'react';
import { mount } from 'enzyme';
import MenuContents from './MenuContents';
import { AuthenticationContext, AuthenticationStatusProps } from '../context/AuthenticationContext';

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
        tenant: 'tenant1',
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

  it('change tenant should redirect', () => {
    const component = mountComponent();
    const tenantSelectorButton = component.find("[data-test='button-change-tenant']").first();
    tenantSelectorButton.simulate('click');
    expect(mockPush).toBeCalledWith('/tenancy/');
  });

  it('tenant name in menu', () => {
    const component = mountComponent();
    const tenantSelectorButton = component.find("[data-test='button-change-tenant']").first();
    expect(tenantSelectorButton.text()).toContain('tenant1');
  });

  it('log out', () => {
    const component = mountComponent();
    const logoutButton = component.find("[data-test='button-logout']").first();
    logoutButton.simulate('click');
    expect(mockSetAuthStatus).toBeCalledWith({ stage: 'Unauthenticated' });
  });
});
