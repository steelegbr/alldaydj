import React from 'react';
import { mount } from 'enzyme';
import Logout from './Logout';

const mockPush = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
}));

describe('logout page', () => {
  const getComponent = () => mount(<Logout />);

  it('clicking log back in redirects', () => {
    const component = getComponent();
    const loginButton = component.find("[data-test='button-login']").first();
    loginButton.simulate('click');
    expect(mockPush).toBeCalledWith('/login/');
  });
});
