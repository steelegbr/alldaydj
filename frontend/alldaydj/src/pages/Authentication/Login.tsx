import {
  Card,
  CardContent,
  FormControl,
  InputLabel,
  InputAdornment,
  Input,
  Button,
  CardHeader,
  CardActions,
  makeStyles,
  createStyles,
  Box,
  FormHelperText,
  CircularProgress,
} from '@material-ui/core';
import { Email, Lock } from '@material-ui/icons';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { userLogin } from '../../api/requests/Authentication';
import { AuthenticationContext } from '../../components/context/AuthenticationContext';
import { Paths } from '../../routing/Paths';
import { loginUser } from '../../services/AuthenticationService';
import { getLogger } from '../../services/LoggingService';
import AuthenticationWrapper from './AuthenticationWrapper';

const useStyles = makeStyles(() => createStyles({
  loginProgress: {
    position: 'absolute',
    left: '50%',
    top: '50%',
    marginLeft: -12,
    marginTop: -12,
  },
  wrapper: {
    position: 'relative',
  },
  errorBox: {
    marginBottom: 10,
    padding: 5,
  },
}));

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
  const classes = useStyles();
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
      email: newLoginStatus.email,
      password: newLoginStatus.password,
    }).then(
      (result) => {
        log.info('User login success!');
        const user = loginUser(result.data.refresh, result.data.access);
        authenticationContext?.setAuthenticationStatus(user);
        history.push(Paths.auth.tenancy);
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

  function loginButton() {
    return (
      <Box className={classes.wrapper}>
        <Button color="primary" disabled={disableButtons} type="submit" variant="contained">
          Login
        </Button>
        {loginStatus.progress === 'InProgress' && (
          <CircularProgress className={classes.loginProgress} size={24} />
        )}
      </Box>
    );
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
        <CardHeader title="Login to AllDay DJ" />
        <CardContent>
          {loginStatus.progress === 'Error' && (
            <Box bgcolor="error.main" boxShadow={3} className={classes.errorBox} data-test="box-error">
              {`Login failed. Please check your username and password and try again. If you continue
              to see this error, please get in touch with support.`}
            </Box>
          )}
          {emailInput()}
          {passwordInput()}
        </CardContent>
        <CardActions>
          {loginButton()}
          <Button
            color="secondary"
            data-test="button-clear"
            disabled={disableButtons}
            onClick={clearForm}
            variant="outlined"
          >
            Clear
          </Button>
        </CardActions>
      </Card>
    );
  }

  return (
    <AuthenticationWrapper>
      <form data-test="form-login" onSubmit={attemptLogin}>
        {loginCard()}
      </form>
    </AuthenticationWrapper>
  );
}
