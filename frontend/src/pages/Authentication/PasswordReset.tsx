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

import {
  Button,
  Card,
  CardActions,
  CardContent,
  FormControl,
  FormHelperText,
  Input,
  InputAdornment,
  InputLabel,
  LinearProgress,
} from '@mui/material';
import { Lock } from '@mui/icons-material';
import { passwordReset, testPasswordResetToken } from 'api/requests/Authentication';
import LoadingButton from 'components/common/LoadingButton';
import React from 'react';
import PasswordStrengthBar from 'react-password-strength-bar';
import { useParams, useNavigate } from 'react-router-dom';
import Paths from 'routing/Paths';
import { getLogger } from 'services/LoggingService';

type ResetState = 'Idle' | 'CheckingToken' | 'TokenNotValid' | 'AwaitingNewPassword' | 'ChangingPassword' | 'Complete' | 'Error'

const PasswordReset = (): React.ReactElement => {
  const navigate = useNavigate();
  const { token } = useParams();
  const [resetRequestState, setResetRequestState] = React.useState<ResetState>('Idle');
  const [password, setPassword] = React.useState<string>('');
  const [repeatPassword, setRepeatPassword] = React.useState<string>('');
  const [passwordStrength, setPasswordStrength] = React.useState<number>(0);
  const passwordsMatch = (password === repeatPassword);
  const passwordStrong = passwordStrength > 1;

  const updatePassword = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const updateRepeatPassword = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    setRepeatPassword(event.target.value);
  };

  const attemptReset = (event: React.SyntheticEvent) => {
    event.preventDefault();
    getLogger().info('Attempting to reset password');
    setResetRequestState('ChangingPassword');

    passwordReset({
      token: token || '',
      password,
    }).then(
      () => {
        getLogger().info('Password reset successful');
        setResetRequestState('Complete');
      },
      (error) => {
        getLogger().warn(`Password reset failed - ${error}`);
        setResetRequestState('Error');
      },
    );
  };

  const returnToLoginScreen = () => {
    navigate(Paths.auth.login);
  };

  const updatePasswordStrength = (strength: number) => {
    setPasswordStrength(strength);
  };

  if (resetRequestState === 'Idle') {
    getLogger().info('Checking password reset token validity');
    setResetRequestState('CheckingToken');
    testPasswordResetToken({ token: token || '' }).then(
      () => {
        setResetRequestState('AwaitingNewPassword');
      },
      (error) => {
        getLogger().warn(`Password reset token check failed - ${error}`);
        setResetRequestState('TokenNotValid');
      },
    );
  }

  const renderPasswordForm = () => (
    <form data-test="form-reset" onSubmit={attemptReset}>
      <Card>
        <CardContent>
          <h1>Reset Password</h1>
          <p>
            Please enter a new password for the account:
          </p>
          <FormControl fullWidth>
            <InputLabel htmlFor="password">
              Password:
            </InputLabel>
            <Input
              data-test="input-password"
              id="password"
              onChange={updatePassword}
              startAdornment={(
                <InputAdornment position="start">
                  <Lock />
                </InputAdornment>
          )}
              type="password"
              value={password}
            />
          </FormControl>
          <FormControl fullWidth>
            <PasswordStrengthBar onChangeScore={updatePasswordStrength} password={password} />
          </FormControl>
          <FormControl fullWidth>
            <InputLabel htmlFor="password">
              Password (again):
            </InputLabel>
            <Input
              data-test="input-repeat-password"
              id="repeat-password"
              onChange={updateRepeatPassword}
              startAdornment={(
                <InputAdornment position="start">
                  <Lock />
                </InputAdornment>
          )}
              type="password"
              value={repeatPassword}
            />
            {!passwordsMatch && (
            <FormHelperText data-test="error-match" error>
              Both passwords must match
            </FormHelperText>
            )}
          </FormControl>
        </CardContent>
        <CardActions>
          <LoadingButton
            aria-label="Reset the password"
            arial-label="Reset Password"
            color="primary"
            data-test="button-reset-password"
            disabled={!(passwordsMatch && passwordStrong)}
            loading={resetRequestState === 'ChangingPassword'}
            type="submit"
            variant="contained"
          >
            Reset Password
          </LoadingButton>
        </CardActions>
      </Card>
    </form>
  );

  const renderLoadingScreen = () => (
    <Card>
      <CardContent>
        <h1>Reset Password</h1>
        <p>
          Checking your token is still valid...
        </p>
        <LinearProgress />
      </CardContent>
    </Card>
  );

  const renderTokenExpired = () => (
    <Card>
      <CardContent>
        <h1>Reset Password</h1>
        <p data-test="message-error">
          Unfortunately, your password reset token has expired.
        </p>
      </CardContent>
      <CardActions>
        <Button
          aria-label="Return to the login screen"
          data-test="button-return-login"
          onClick={returnToLoginScreen}
          type="submit"
          variant="contained"
        >
          Return to Login Screen
        </Button>
      </CardActions>
    </Card>
  );

  const renderCompleteScreen = () => (
    <Card>
      <CardContent>
        <h1>Reset Password</h1>
        <p data-test="message-success">
          Password reset successful.
        </p>
      </CardContent>
      <CardActions>
        <Button
          aria-label="Return to the login screen"
          data-test="button-return-login"
          onClick={returnToLoginScreen}
          type="submit"
          variant="contained"
        >
          Return to Login Screen
        </Button>
      </CardActions>
    </Card>
  );

  const renderErrorScreen = () => (
    <Card>
      <CardContent>
        <h1>Reset Password</h1>
        <p data-test="message-error">
          Unfortunately something went wrong with the password reset.
        </p>
      </CardContent>
      <CardActions>
        <Button
          aria-label="Return to the login screen"
          data-test="button-return-login"
          onClick={returnToLoginScreen}
          type="submit"
          variant="contained"
        >
          Return to Login Screen
        </Button>
      </CardActions>
    </Card>
  );

  if (resetRequestState === 'Idle' || resetRequestState === 'CheckingToken') {
    return renderLoadingScreen();
  }

  if (resetRequestState === 'TokenNotValid') {
    return renderTokenExpired();
  }

  if (resetRequestState === 'Error') {
    return renderErrorScreen();
  }

  if (resetRequestState === 'Complete') {
    return renderCompleteScreen();
  }

  return renderPasswordForm();
};

export default PasswordReset;
