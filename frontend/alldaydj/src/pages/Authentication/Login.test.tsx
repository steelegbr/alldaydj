import React from 'react';
import { mount } from 'enzyme';
import { act } from '@testing-library/react';
import Login from './Login';
import { userLogin } from '../../api/requests/Authentication';
import { loginUser } from '../../services/AuthenticationService';
import { AuthenticationStatus } from '../../components/context/AuthenticationContext';

const mockUserLogin = userLogin as jest.Mock;
const mockLoginUser = loginUser as jest.Mock;
const mockPush = jest.fn();

jest.mock('../../api/requests/Authentication');
jest.mock('../../services/AuthenticationService');
jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
}));

describe('login page', () => {
  const getComponent = () => mount(<Login />);

  beforeAll(() => {
    jest.resetAllMocks();
  });

  it('login fails without a username and password', () => {
    const component = getComponent();
    const loginForm = component.find("form[data-test='form-login']");

    loginForm.simulate('submit');
    component.update();

    const emailError = component.find("[data-test='error-email']").first();
    const passwordError = component.find("[data-test='error-password']").first();

    expect(emailError.getDOMNode().textContent).toBe('You must supply a username');
    expect(passwordError.getDOMNode().textContent).toBe('You must supply a password');
  });

  it('successful login redirects', async () => {
    const loginSuccess = Promise.resolve({
      data: {
        refresh: 'token1',
        access: 'token2',
      },
    });

    const authStatus : AuthenticationStatus = {
      stage: 'Authenticated',
    };

    mockUserLogin.mockReturnValue(loginSuccess);
    mockLoginUser.mockReturnValue(authStatus);

    const component = getComponent();
    const emailInput = component.find("[data-test='input-email']").find('input');
    const passwordInput = component.find("[data-test='input-password']").find('input');

    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    passwordInput.simulate('change', { target: { value: 'p@55w0rd1' } });

    component.update();

    const loginForm = component.find("form[data-test='form-login']");
    loginForm.simulate('submit');

    await act(async () => {
      await loginSuccess;
    });

    expect(mockPush).toBeCalledWith('/tenancy/');
  });

  it('login failure presents an error message', async () => {
    const loginFail = Promise.reject(new Error('Bad Credentials'));
    mockUserLogin.mockReturnValue(loginFail);

    const component = getComponent();
    const emailInput = component.find("[data-test='input-email']").find('input');
    const passwordInput = component.find("[data-test='input-password']").find('input');

    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    passwordInput.simulate('change', { target: { value: 'p@55w0rd1' } });

    component.update();

    const loginForm = component.find("form[data-test='form-login']");
    loginForm.simulate('submit');

    await act(async () => {
      await mockUserLogin;
    });

    component.update();

    const errorBox = component.find("[data-test='box-error']").last();
    expect(errorBox.getDOMNode().textContent).toContain('Login failed.');
  });

  it('clear button clears the form', () => {
    const loginFail = Promise.reject(new Error('Bad Credentials'));
    mockUserLogin.mockReturnValue(loginFail);

    const component = getComponent();
    const emailInput = component.find("[data-test='input-email']").find('input');
    const passwordInput = component.find("[data-test='input-password']").find('input');

    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    passwordInput.simulate('change', { target: { value: 'p@55w0rd1' } });

    component.update();

    const clearButton = component.find("[data-test='button-clear']").find('button');
    clearButton.simulate('click');
    component.update();

    const updatedEmailInput = component.find("[data-test='input-email']").find('input');
    const updatedPasswordInput = component.find("[data-test='input-password']").find('input');

    expect(updatedEmailInput.getDOMNode().getAttribute('value')).toEqual('');
    expect(updatedPasswordInput.getDOMNode().getAttribute('value')).toEqual('');
  });
});
