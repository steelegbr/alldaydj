import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dummy from '../components/test/Dummy';
import AuthenticationWrapper from './AuthenticationWrapper';
import Login from '../pages/Authentication/Login';
import Paths from './Paths';
import PrivateRoute from './PrivateRoute';
import StandardWrapper from './StandardWrapper';
import Library from '../pages/Library/Library';
import Logout from '../pages/Authentication/Logout';
import { CartSearchProvider } from '../components/context/CartSearchContext';

export default function ApplicationRouter() : React.ReactElement {
  return (
    <Switch>
      <Route path={Paths.auth.login}>
        <AuthenticationWrapper>
          <Login />
        </AuthenticationWrapper>
      </Route>
      <Route path={Paths.auth.logout}>
        <AuthenticationWrapper>
          <Logout />
        </AuthenticationWrapper>
      </Route>
      <PrivateRoute path={Paths.library.search}>
        <StandardWrapper>
          <CartSearchProvider>
            <Library />
          </CartSearchProvider>
        </StandardWrapper>
      </PrivateRoute>
      <PrivateRoute path={Paths.base}>
        <StandardWrapper>
          <Dummy />
        </StandardWrapper>
      </PrivateRoute>
    </Switch>
  );
}
