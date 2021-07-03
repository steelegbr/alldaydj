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
  Card,
  CardContent,
  FormControl,
  InputLabel,
  InputAdornment,
  Input,
  Button,
  CardActions,
  FormHelperText,
  Snackbar,
} from '@material-ui/core';
import { Email, Lock } from '@material-ui/icons';
import { Alert } from '@material-ui/lab';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { userLogin } from 'api/requests/Authentication';
import LoadingButton from 'components/common/LoadingButton';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import Paths from 'routing/Paths';
import { loginUser } from 'services/AuthenticationService';
import { getLogger } from 'services/LoggingService';

type LoginProgress = 'Idle' | 'Error' | 'InProgress' | 'Failed';

interface LoginStatus {
  progress: LoginProgress;
  errorEmail?: string;
  errorPassword?: string;
  email: string;
  password: string;
}

export default function Login(): React.ReactElement {
  const log = getLogger();
  const history = useHistory();
  const authenticationContext = React.useContext(AuthenticationContext);
  const [loginStatus, setLoginStatus] = React.useState<LoginStatus>({
    progress: 'Idle',
    email: '',
    password: '',
  });
  const disableButtons = loginStatus.progress === 'InProgress';

  function setEmail(email: string) {
    setLoginStatus({
      ...loginStatus,
      errorEmail: undefined,
      email,
    });
  }

  function setPassword(password: string) {
    setLoginStatus({
      ...loginStatus,
      errorPassword: undefined,
      password,
    });
  }

  function clearForm() {
    setLoginStatus({
      progress: 'Idle',
      email: '',
      password: '',
      errorEmail: undefined,
      errorPassword: undefined,
    });
    log.info('Cleared the login form');
  }

  function doSetEmail(event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) {
    setEmail(event.target.value);
  }

  function doSetPassword(event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) {
    setPassword(event.target.value);
  }

  function attemptLogin(event: React.SyntheticEvent) {
    event.preventDefault();

    const newLoginStatus: LoginStatus = {
      progress: 'InProgress',
      email: loginStatus.email,
      password: loginStatus.password,
    };

    log.info('Starting login validation.');

    let errors = false;

    if (!loginStatus.email) {
      newLoginStatus.errorEmail = 'You must supply a username';
      errors = true;
    }

    if (!loginStatus.password) {
      newLoginStatus.errorPassword = 'You must supply a password';
      errors = true;
    }

    if (errors) {
      newLoginStatus.progress = 'Idle';
      setLoginStatus(newLoginStatus);
      log.error('Login validation failed!');
      return;
    }

    log.info('Login validation complete.');
    setLoginStatus(newLoginStatus);

    userLogin({
      username: newLoginStatus.email,
      password: newLoginStatus.password,
    }).then(
      (result) => {
        log.info('User login success!');
        const user = loginUser(result.data.refresh, result.data.access);
        authenticationContext?.setAuthenticationStatus(user);
        history.push(Paths.base);
      },
      (error) => {
        log.warn(`User login failed - ${error}`);
        setLoginStatus({
          ...newLoginStatus,
          progress: 'Error',
        });
      },
    );
  }

  function forgottenPassword() {
    history.push(Paths.auth.forgottenPassword);
  }

  function emailInput() {
    return (
      <FormControl fullWidth>
        <InputLabel htmlFor="email">
          Username (e-mail):
        </InputLabel>
        <Input
          data-test="input-email"
          error={loginStatus.errorEmail !== undefined}
          id="email"
          onChange={doSetEmail}
          startAdornment={(
            <InputAdornment position="start">
              <Email />
            </InputAdornment>
          )}
          type="email"
          value={loginStatus.email}
        />
        {loginStatus.errorEmail && (
          <FormHelperText data-test="error-email" error>
            {loginStatus.errorEmail}
          </FormHelperText>
        )}
      </FormControl>
    );
  }

  function passwordInput() {
    return (
      <FormControl fullWidth>
        <InputLabel htmlFor="password">
          Password:
        </InputLabel>
        <Input
          data-test="input-password"
          error={loginStatus.errorPassword !== undefined}
          id="password"
          onChange={doSetPassword}
          startAdornment={(
            <InputAdornment position="start">
              <Lock />
            </InputAdornment>
          )}
          type="password"
          value={loginStatus.password}
        />
        {loginStatus.errorPassword && (
          <FormHelperText data-test="error-password" error>
            {loginStatus.errorPassword}
          </FormHelperText>
        )}
      </FormControl>
    );
  }

  function loginCard() {
    return (
      <Card>
        <CardContent>
          <h1>Login to AllDay DJ</h1>
          <Snackbar autoHideDuration={6000} data-test="box-error" open={loginStatus.progress === 'Error'}>
            <Alert elevation={6} severity="error" variant="filled">
              {`Login failed. Please check your username and password and try again. If you continue
              to see this error, please get in touch with support.`}
            </Alert>
          </Snackbar>
          {emailInput()}
          {passwordInput()}
        </CardContent>
        <CardActions>
          <LoadingButton arial-label="Login" color="primary" loading={disableButtons} type="submit" variant="contained">
            Login
          </LoadingButton>
          <Button
            aria-label="Clear the login form"
            color="secondary"
            data-test="button-clear"
            disabled={disableButtons}
            onClick={clearForm}
            variant="contained"
          >
            Clear
          </Button>
          <Button
            aria-label="Request a password reset"
            data-test="button-reset"
            onClick={forgottenPassword}
          >
            Forgotten Password?
          </Button>
        </CardActions>
      </Card>
    );
  }

  return (
    <form data-test="form-login" onSubmit={attemptLogin}>
      {loginCard()}
    </form>
  );
}
