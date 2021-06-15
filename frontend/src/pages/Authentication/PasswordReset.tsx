import {
  Card, CardContent, FormControl, Input, InputAdornment, InputLabel,
} from '@material-ui/core';
import { Lock } from '@material-ui/icons';
import React from 'react';
import PasswordStrengthBar from 'react-password-strength-bar';
// import { useParams } from 'react-router-dom';

// type PasswordResetParams = {
//    token: string
// }

const PasswordReset = (): React.ReactElement => {
  // const { token } = useParams<PasswordResetParams>();
  const [password, setPassword] = React.useState<string>('');
  const [repeatPassword, setRepeatPassword] = React.useState<string>('');

  const updatePassword = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const updateRepeatPassword = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    setRepeatPassword(event.target.value);
  };

  const attemptReset = (event: React.SyntheticEvent) => {
    event.preventDefault();
  };

  return (
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
            <PasswordStrengthBar password={password} />
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
          </FormControl>
        </CardContent>
      </Card>
    </form>
  );
};

export default PasswordReset;
