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
import ForgottenPassword from 'pages/Authentication/ForgottenPassword';
import { forgottenPassword } from 'api/requests/Authentication';
import { act } from '@testing-library/react';

const mockForgottenPassword = forgottenPassword as jest.Mock;
jest.mock('api/requests/Authentication');

describe('forgotten password', () => {
  const getComponent = () => mount(<ForgottenPassword />);

  beforeAll(() => {
    jest.resetAllMocks();
  });

  it('reset fails without an e-mail address', () => {
    const component = getComponent();
    const resetForm = component.find("form[data-test='form-reset']");

    resetForm.simulate('submit');
    component.update();

    const emailError = component.find("[data-test='error-email']").first();
    expect(emailError.getDOMNode().textContent).toBe('You must supply an e-mail address');
  });

  it('clear button clears the form', () => {
    const component = getComponent();
    const emailInput = component.find("[data-test='input-email']").find('input');

    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    component.update();

    const clearButton = component.find("[data-test='button-clear']").find('button');
    clearButton.simulate('click');
    component.update();

    const updatedEmailInput = component.find("[data-test='input-email']").find('input');
    expect(updatedEmailInput.getDOMNode().getAttribute('value')).toEqual('');
  });

  it('successful request renders info box', async () => {
    const component = getComponent();
    const resetRequest = Promise.resolve({
      data: {},
    });
    mockForgottenPassword.mockReturnValue(resetRequest);

    const emailInput = component.find("[data-test='input-email']").find('input');
    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    component.update();

    const resetForm = component.find("form[data-test='form-reset']");
    resetForm.simulate('submit');

    await act(async () => {
      await resetRequest;
    });

    component.update();

    const infoBox = component.find("[data-test='box-info']").last();
    expect(infoBox.getDOMNode().textContent).toContain('If the account exists, an e-mail has been sent to the account.');
    expect(mockForgottenPassword).toBeCalledWith({
      email: 'user@example.com',
    });
  });

  it('bad request renders error box', async () => {
    const component = getComponent();
    const resetRequest = Promise.reject(new Error('Whoops!'));
    mockForgottenPassword.mockReturnValue(resetRequest);

    const emailInput = component.find("[data-test='input-email']").find('input');
    emailInput.simulate('change', { target: { value: 'user@example.com' } });
    component.update();

    const resetForm = component.find("form[data-test='form-reset']");
    resetForm.simulate('submit');

    await act(async () => {
      await mockForgottenPassword;
    });

    component.update();

    const errorBox = component.find("[data-test='box-error']").last();
    expect(errorBox.getDOMNode().textContent).toContain('Password reset failed. Please try again later or contact an administrator for help.');
    expect(mockForgottenPassword).toBeCalledWith({
      email: 'user@example.com',
    });
  });
});
