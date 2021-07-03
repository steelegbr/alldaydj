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
import { act } from '@testing-library/react';
import { passwordReset, testPasswordResetToken } from 'api/requests/Authentication';
import PasswordReset from 'pages/Authentication/PasswordReset';
import { mount } from 'enzyme';

const mockTestPasswordResetToken = testPasswordResetToken as jest.Mock;
const mockPasswordReset = passwordReset as jest.Mock;
jest.mock('api/requests/Authentication');

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({
    token: 'abc123',
  }),
}));

describe('password reset', () => {
  const getComponent = () => mount(<PasswordReset />);

  beforeAll(() => {
    jest.resetAllMocks();
  });

  it('bad token displays error', async () => {
    const badRequest = Promise.reject(new Error('Bad Token'));
    mockTestPasswordResetToken.mockReturnValue(badRequest);
    const component = getComponent();

    await act(async () => {
      await mockTestPasswordResetToken;
    });

    component.update();

    const errorText = component.find("[data-test='message-error']").last();
    expect(errorText.getDOMNode().textContent).toContain('Unfortunately, your password reset token has expired.');
    expect(mockTestPasswordResetToken).toBeCalledWith({ token: 'abc123' });
  });

  it('passwords must match', async () => {
    mockTestPasswordResetToken.mockReturnValue(Promise.resolve());
    const component = getComponent();

    // Let the valid token request happen

    await act(async () => {
      await mockTestPasswordResetToken;
    });

    component.update();

    // Give the mismatched passwords

    const passwordBox = component.find("[data-test='input-password']").find('input');
    const passwordRepeatBox = component.find("[data-test='input-repeat-password']").find('input');
    passwordBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re!' } });
    passwordRepeatBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re?' } });
    component.update();

    const submitButton = component.find("[data-test='button-reset-password']").find('button');
    expect(submitButton.getDOMNode()).toBeDisabled();

    const errorMatch = component.find("[data-test='error-match']").first();
    expect(errorMatch.getDOMNode().textContent).toBe('Both passwords must match');
    expect(mockTestPasswordResetToken).toBeCalledWith({ token: 'abc123' });
  });

  it('passwords must be secure', async () => {
    mockTestPasswordResetToken.mockReturnValue(Promise.resolve());
    const component = getComponent();

    // Let the valid token request happen

    await act(async () => {
      await mockTestPasswordResetToken;
    });

    component.update();

    // Give the insecure but matching passwords

    const passwordBox = component.find("[data-test='input-password']").find('input');
    const passwordRepeatBox = component.find("[data-test='input-repeat-password']").find('input');
    passwordBox.simulate('change', { target: { value: 'password' } });
    passwordRepeatBox.simulate('change', { target: { value: 'password' } });
    component.update();

    const submitButton = component.find("[data-test='button-reset-password']").find('button');
    expect(submitButton.getDOMNode()).toBeDisabled();
    expect(mockTestPasswordResetToken).toBeCalledWith({ token: 'abc123' });
  });

  it('error on resetting password', async () => {
    mockTestPasswordResetToken.mockReturnValue(Promise.resolve());
    mockPasswordReset.mockRejectedValue(new Error('Error'));
    const component = getComponent();

    // Let the valid token request happen

    await act(async () => {
      await mockTestPasswordResetToken;
    });

    component.update();

    // Give the passwords

    const passwordBox = component.find("[data-test='input-password']").find('input');
    const passwordRepeatBox = component.find("[data-test='input-repeat-password']").find('input');
    passwordBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re!' } });
    passwordRepeatBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re!' } });
    component.update();

    const resetForm = component.find("form[data-test='form-reset']");
    resetForm.simulate('submit');

    // Simulated call to reset the password

    await act(async () => {
      await mockPasswordReset;
    });

    component.update();

    // Check we land in the right place

    const errorText = component.find("[data-test='message-error']").last();
    expect(errorText.getDOMNode().textContent).toContain('Unfortunately something went wrong with the password reset.');
    expect(mockPasswordReset).toBeCalledWith({ password: '$ecureP@55Go3sH3re!', token: 'abc123' });
    expect(mockTestPasswordResetToken).toBeCalledWith({ token: 'abc123' });
  });

  it('happy path', async () => {
    mockTestPasswordResetToken.mockReturnValue(Promise.resolve());
    mockPasswordReset.mockReturnValue(Promise.resolve());
    const component = getComponent();

    // Let the valid token request happen

    await act(async () => {
      await mockTestPasswordResetToken;
    });

    component.update();

    // Give the passwords

    const passwordBox = component.find("[data-test='input-password']").find('input');
    const passwordRepeatBox = component.find("[data-test='input-repeat-password']").find('input');
    passwordBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re!' } });
    passwordRepeatBox.simulate('change', { target: { value: '$ecureP@55Go3sH3re!' } });
    component.update();

    const resetForm = component.find("form[data-test='form-reset']");
    resetForm.simulate('submit');

    // Simulated call to reset the password

    await act(async () => {
      await mockPasswordReset;
    });

    component.update();

    // Check we land in the right place

    const infoText = component.find("[data-test='message-success']").last();
    expect(infoText.getDOMNode().textContent).toContain('Password reset successful.');
    expect(mockPasswordReset).toBeCalledWith({ password: '$ecureP@55Go3sH3re!', token: 'abc123' });
    expect(mockTestPasswordResetToken).toBeCalledWith({ token: 'abc123' });
  });
});
