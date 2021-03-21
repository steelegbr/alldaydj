import {
  Button, Card, CardActions, CardContent, Typography,
} from '@material-ui/core';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import Paths from 'routing/Paths';
import { logOut } from 'services/AuthenticationService';

const Logout = (): React.ReactElement => {
  const history = useHistory();
  const authenticationContext = React.useContext(AuthenticationContext);
  if (authenticationContext?.authenticationStatus.stage !== 'Unauthenticated') {
    authenticationContext?.setAuthenticationStatus(logOut());
  }

  const redirectToLogin = () => {
    history.push(Paths.auth.login);
  };

  return (
    <Card>
      <CardContent>
        <h1>Log Out</h1>
        <Typography>
          You have successfully logged out of AllDay DJ.
        </Typography>
      </CardContent>
      <CardActions>
        <Button
          color="primary"
          data-test="button-login"
          onClick={redirectToLogin}
          variant="contained"
        >
          Log In
        </Button>
      </CardActions>
    </Card>
  );
};

export default Logout;
