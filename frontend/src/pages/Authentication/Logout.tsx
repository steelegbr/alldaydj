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
