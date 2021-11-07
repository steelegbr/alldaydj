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
  Alert,
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
} from '@mui/material';
import { Email, Lock } from '@mui/icons-material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
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

const useStyles = makeStyles(() => createStyles({
  loginButton: {
    marginRight: 10,
  },
}));

export default function Login(): React.ReactElement {
  const navigate = useNavigate();
  const classes = useStyles();
  const authenticationContext = React.useContext(AuthenticationContext);
  const [loginStatus, setLoginStatus] = React.useState<LoginStatus>({
    progress: 'Idle',
    email: '',
    password: '',
  });
  const disableButtons = loginStatus.progress === 'InProgress';

  const setEmail = useCallback(
    (email: string) => {
      setLoginStatus({
        ...loginStatus,
        errorEmail: undefined,
        email,
      });
    },
    [loginStatus, setLoginStatus],
  );

  const setPassword = useCallback(
    (password: string) => {
      setLoginStatus({
        ...loginStatus,
        errorPassword: undefined,
        password,
      });
    },
    [loginStatus, setLoginStatus],
  );

  const clearForm = useCallback(
    () => {
      setLoginStatus({
        progress: 'Idle',
        email: '',
        password: '',
        errorEmail: undefined,
        errorPassword: undefined,
      });
      getLogger().info('Cleared the login form');
    },
    [setLoginStatus],
  );

  const doSetEmail = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
      setEmail(event.target.value);
    },
    [setEmail],
  );

  const doSetPassword = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
      setPassword(event.target.value);
    },
    [setPassword],
  );

  const attemptLogin = useCallback(
    (event: React.SyntheticEvent) => {
      event.preventDefault();

      const newLoginStatus: LoginStatus = {
        progress: 'InProgress',
        email: loginStatus.email,
        password: loginStatus.password,
      };

      getLogger().info('Starting login validation.');

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
        getLogger().error('Login validation failed!');
        return;
      }

      getLogger().info('Login validation complete.');
      setLoginStatus(newLoginStatus);

      userLogin({
        username: newLoginStatus.email,
        password: newLoginStatus.password,
      }).then(
        (result) => {
          getLogger().info('User login success!');
          const user = loginUser(result.data.refresh, result.data.access);
          authenticationContext?.setAuthenticationStatus(user);
          navigate(Paths.base);
        },
        (error) => {
          getLogger().warn(`User login failed - ${error}`);
          setLoginStatus({
            ...newLoginStatus,
            progress: 'Error',
          });
        },
      );
    },
    [authenticationContext, navigate, loginStatus],
  );

  const forgottenPassword = useCallback(
    () => {
      navigate(Paths.auth.forgottenPassword);
    },
    [navigate],
  );

  function emailInput() {
    return (
      <FormControl fullWidth variant="standard">
        <InputLabel htmlFor="email">
          Username (e-mail):
        </InputLabel>
        <Input
          data-test="input-email"
          error={loginStatus.errorEmail !== undefined}
          id="email"
          margin="none"
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
      <FormControl fullWidth variant="standard">
        <InputLabel htmlFor="password">
          Password:
        </InputLabel>
        <Input
          data-test="input-password"
          error={loginStatus.errorPassword !== undefined}
          id="password"
          margin="none"
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
          <LoadingButton arial-label="Login" className={classes.loginButton} color="primary" loading={disableButtons} type="submit" variant="contained">
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
            color="secondary"
            data-test="button-reset"
            onClick={forgottenPassword}
            variant="contained"
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
