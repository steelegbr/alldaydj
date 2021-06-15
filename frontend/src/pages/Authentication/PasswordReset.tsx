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
} from '@material-ui/core';
import { Lock } from '@material-ui/icons';
import { passwordReset, testPasswordResetToken } from 'api/requests/Authentication';
import LoadingButton from 'components/common/LoadingButton';
import React from 'react';
import PasswordStrengthBar from 'react-password-strength-bar';
import { useParams, useHistory } from 'react-router-dom';
import Paths from 'routing/Paths';
import { getLogger } from 'services/LoggingService';

type PasswordResetParams = {
    token: string
}

type ResetState = 'Idle' | 'CheckingToken' | 'TokenNotValid' | 'AwaitingNewPassword' | 'ChangingPassword' | 'Complete' | 'Error'

const PasswordReset = (): React.ReactElement => {
  const log = getLogger();
  const history = useHistory();
  const { token } = useParams<PasswordResetParams>();
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
    log.info('Attempting to reset password');
    setResetRequestState('ChangingPassword');

    passwordReset({
      token,
      password,
    }).then(
      () => {
        log.info('Password reset successful');
        setResetRequestState('Complete');
      },
      (error) => {
        log.warn(`Password reset failed - ${error}`);
        setResetRequestState('Error');
      },
    );
  };

  const returnToLoginScreen = () => {
    history.push(Paths.auth.login);
  };

  const updatePasswordStrength = (strength: number) => {
    setPasswordStrength(strength);
  };

  if (resetRequestState === 'Idle') {
    log.info('Checking password reset token validity');
    setResetRequestState('CheckingToken');
    testPasswordResetToken({ token }).then(
      () => {
        setResetRequestState('AwaitingNewPassword');
      },
      (error) => {
        log.warn(`Password reset token check failed - ${error}`);
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
        <p>
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
        <p>
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
        <p>
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
