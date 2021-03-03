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
