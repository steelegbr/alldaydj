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

import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Dummy from 'components/test/Dummy';
import AuthenticationWrapper from 'routing/AuthenticationWrapper';
import Login from 'pages/Authentication/Login';
import Paths from 'routing/Paths';
import PrivateRoute from 'routing/PrivateRoute';
import StandardWrapper from 'routing/StandardWrapper';
import Library from 'pages/Library/Library';
import Logout from 'pages/Authentication/Logout';
import { CartSearchProvider } from 'components/context/CartSearchContext';
import ForgottenPassword from 'pages/Authentication/ForgottenPassword';
import PasswordReset from 'pages/Authentication/PasswordReset';
import CartEditor from 'pages/Cart/CartEditor';
import { CartEditorProvider } from 'components/context/CartEditorContext';
import CartSynchroniser from 'pages/Cart/CartSynchroniser';

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
      <Route path={Paths.auth.forgottenPassword}>
        <AuthenticationWrapper>
          <ForgottenPassword />
        </AuthenticationWrapper>
      </Route>
      <Route path={`${Paths.auth.passwordReset}:token`}>
        <AuthenticationWrapper>
          <PasswordReset />
        </AuthenticationWrapper>
      </Route>
      <PrivateRoute path={Paths.library.search}>
        <StandardWrapper>
          <CartSearchProvider>
            <Library />
          </CartSearchProvider>
        </StandardWrapper>
      </PrivateRoute>
      <PrivateRoute path={`${Paths.cart}:cartId`}>
        <StandardWrapper>
          <CartEditorProvider>
            <CartEditor />
          </CartEditorProvider>
        </StandardWrapper>
      </PrivateRoute>
      <PrivateRoute path={Paths.cart}>
        <StandardWrapper>
          <CartEditorProvider>
            <CartEditor />
          </CartEditorProvider>
        </StandardWrapper>
      </PrivateRoute>
      <PrivateRoute path={Paths.cartSync}>
        <StandardWrapper>
          <CartSynchroniser />
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
