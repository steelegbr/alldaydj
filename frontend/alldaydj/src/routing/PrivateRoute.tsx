/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
import { AuthenticationContext } from '../components/context/AuthenticationContext';
import { isAuthenticated } from '../services/AuthenticationService';
import { getLogger } from '../services/LoggingService';
import Paths from './Paths';

export default function PrivateRoute(props: RouteProps): React.ReactElement {
  const authenticationContext = React.useContext(AuthenticationContext);
  const authenticated = isAuthenticated(authenticationContext);
  const log = getLogger();

  if (authenticated) {
    return <Route {...props} />;
  }

  log.warn('Attempt to access private route while not authenticated!');
  return (
    <Route {...props}>
      <Redirect to={Paths.auth.login} />
    </Route>
  );
}
