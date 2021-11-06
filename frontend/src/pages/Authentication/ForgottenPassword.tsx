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
  Button,
  Card,
  CardActions,
  CardContent,
  FormControl, FormHelperText, Input, InputAdornment, InputLabel, Snackbar,
} from '@mui/material';
import { Email } from '@mui/icons-material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import { forgottenPassword } from 'api/requests/Authentication';
import LoadingButton from 'components/common/LoadingButton';
import React from 'react';
import { getLogger } from 'services/LoggingService';

type RequestState = 'Idle' | 'InFlight' | 'Complete' | 'Error'

const useStyles = makeStyles(() => createStyles({
  resetButton: {
    marginRight: 10,
  },
}));

const ForgottenPassword = (): React.ReactElement => {
  const classes = useStyles();

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

    getLogger().info('Starting password reset validation');

    if (!email) {
      setErrorEmail('You must supply an e-mail address');
      setRequestState('Idle');
      getLogger().error('Password reset validation failed.');
      return;
    }

    forgottenPassword({ email }).then(
      () => {
        getLogger().info('Password reset request success.');
        setRequestState('Complete');
      },
      (error) => {
        getLogger().warn(`Password reset request failed - ${error}`);
        setRequestState('Error');
      },
    );
  };

  return (
    <form data-test="form-reset" onSubmit={attemptReset}>
      <Card>
        <CardContent>
          <h1>Forgotten Password</h1>
          <Snackbar autoHideDuration={6000} data-test="box-info" open={requestState === 'Complete'}>
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
          <FormControl fullWidth variant="standard">
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
          <LoadingButton arial-label="Reset" className={classes.resetButton} color="primary" loading={requestState === 'InFlight'} type="submit" variant="contained">
            Reset
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
