import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dummy from '../components/test/Dummy';
import AuthenticationWrapper from './AuthenticationWrapper';
import Login from '../pages/Authentication/Login';
import Paths from './Paths';
import PrivateRoute from './PrivateRoute';
import StandardWrapper from './StandardWrapper';

export default function ApplicationRouter() : React.ReactElement {
  return (
    <Switch>
      <Route path={Paths.auth.login}>
        <AuthenticationWrapper>
          <Login />
        </AuthenticationWrapper>
      </Route>
      <PrivateRoute path={Paths.base}>
        <StandardWrapper>
          <Dummy />
        </StandardWrapper>
      </PrivateRoute>
    </Switch>
  );
}
