import {
  Button,
  Card,
  CardActions,
  CardContent,
  FormControl, FormHelperText, Input, InputAdornment, InputLabel, Snackbar,
} from '@material-ui/core';
import { Email } from '@material-ui/icons';
import { Alert } from '@material-ui/lab';
import { forgottenPassword } from 'api/requests/Authentication';
import LoadingButton from 'components/common/LoadingButton';
import React from 'react';
import { getLogger } from 'services/LoggingService';

type RequestState = 'Idle' | 'InFlight' | 'Complete' | 'Error'

const ForgottenPassword = (): React.ReactElement => {
  const log = getLogger();
  const [requestState, setRequestState] = React.useState<RequestState>('Idle');
  const [email, setEmail] = React.useState<string>('');
  const [errorEmail, setErrorEmail] = React.useState<string|undefined>();

  const updateEmail = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const clearForm = () => {
    setEmail('');
    setRequestState('Idle');
    setErrorEmail(undefined);
  };

  const attemptReset = (event: React.SyntheticEvent) => {
    event.preventDefault();
    setRequestState('InFlight');
    setErrorEmail('');

    log.info('Starting password reset validation');

    if (!email) {
      setErrorEmail('You must supply an e-mail address');
      setRequestState('Idle');
      log.error('Password reset validation failed.');
      return;
    }

    forgottenPassword({ email }).then(
      () => {
        log.info('Password reset request success.');
        setRequestState('Complete');
      },
      (error) => {
        log.warn(`Password reset request failed - ${error}`);
        setRequestState('Error');
      },
    );
  };

  return (
    <form data-test="form-reset" onSubmit={attemptReset}>
      <Card>
        <CardContent>
          <h1>Forgotten Password</h1>
          <Snackbar autoHideDuration={6000} data-test="box-error" open={requestState === 'Complete'}>
            <Alert elevation={6} severity="info" variant="filled">
              If the account exists, an e-mail has been sent to the account.
            </Alert>
          </Snackbar>
          <Snackbar autoHideDuration={6000} data-test="box-error" open={requestState === 'Error'}>
            <Alert elevation={6} severity="error" variant="filled">
              Password reset failed. Please try again later or contact an administrator for help.
            </Alert>
          </Snackbar>
          <p>
            Please enter the e-mail address of the account you have forgotten the password for.
          </p>
          <FormControl fullWidth>
            <InputLabel htmlFor="email">
              Username (e-mail):
            </InputLabel>
            <Input
              data-test="input-email"
              id="email"
              onChange={updateEmail}
              startAdornment={(
                <InputAdornment position="start">
                  <Email />
                </InputAdornment>
          )}
              type="email"
              value={email}
            />
            {errorEmail && (
            <FormHelperText data-test="error-email" error>
              {errorEmail}
            </FormHelperText>
            )}
          </FormControl>
        </CardContent>
        <CardActions>
          <LoadingButton arial-label="Login" color="primary" loading={requestState === 'InFlight'} type="submit" variant="contained">
            Login
          </LoadingButton>
          <Button
            aria-label="Clear the login form"
            color="secondary"
            data-test="button-clear"
            disabled={requestState === 'InFlight'}
            onClick={clearForm}
            variant="contained"
          >
            Clear
          </Button>
        </CardActions>
      </Card>
    </form>
  );
};

export default ForgottenPassword;
