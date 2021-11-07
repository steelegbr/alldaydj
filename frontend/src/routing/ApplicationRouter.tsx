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
import { Navigate, Route, Routes } from 'react-router-dom';
import Dummy from 'components/test/Dummy';
import AuthenticationWrapper from 'routing/AuthenticationWrapper';
import Login from 'pages/Authentication/Login';
import Paths from 'routing/Paths';
import StandardWrapper from 'routing/StandardWrapper';
import Library from 'pages/Library/Library';
import Logout from 'pages/Authentication/Logout';
import { CartSearchProvider } from 'components/context/CartSearchContext';
import ForgottenPassword from 'pages/Authentication/ForgottenPassword';
import PasswordReset from 'pages/Authentication/PasswordReset';
import CartEditor from 'pages/Cart/CartEditor';
import { CartEditorProvider } from 'components/context/CartEditorContext';
import CartSynchroniser from 'pages/Cart/CartSynchroniser';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import { isAuthenticated } from 'services/AuthenticationService';

export default function ApplicationRouter() : React.ReactElement {
  const authenticationContext = React.useContext(AuthenticationContext);
  const authenticated = isAuthenticated(authenticationContext);

  return (
    <Routes>
      <Route
        element={(
          <AuthenticationWrapper>
            <Login />
          </AuthenticationWrapper>
        )}
        path={Paths.auth.login}
      />
      <Route
        element={(
          <AuthenticationWrapper>
            <Logout />
          </AuthenticationWrapper>
        )}
        path={Paths.auth.logout}
      />
      <Route
        element={(
          <AuthenticationWrapper>
            <ForgottenPassword />
          </AuthenticationWrapper>
      )}
        path={Paths.auth.forgottenPassword}
      />
      <Route
        element={(
          <AuthenticationWrapper>
            <PasswordReset />
          </AuthenticationWrapper>
      )}
        path={`${Paths.auth.passwordReset}:token`}
      />
      <Route
        element={(
          authenticated ? (
            <StandardWrapper>
              <CartSearchProvider>
                <Library />
              </CartSearchProvider>
            </StandardWrapper>
          ) : <Navigate to={Paths.auth.login} />
      )}
        path={Paths.library.search}
      />
      <Route
        element={(
          authenticated ? (
            <StandardWrapper>
              <CartEditorProvider>
                <CartEditor />
              </CartEditorProvider>
            </StandardWrapper>
          ) : <Navigate to={Paths.auth.login} />
      )}
        path={`${Paths.cart}:cartId`}
      />
      <Route
        element={(
          authenticated ? (
            <StandardWrapper>
              <CartEditorProvider>
                <CartEditor />
              </CartEditorProvider>
            </StandardWrapper>
          ) : <Navigate to={Paths.auth.login} />
      )}
        path={Paths.cart}
      />
      <Route
        element={(
          authenticated ? (
            <StandardWrapper>
              <CartSynchroniser />
            </StandardWrapper>
          ) : <Navigate to={Paths.auth.login} />
      )}
        path={Paths.cartSync}
      />
      <Route
        element={(
          authenticated ? (
            <StandardWrapper>
              <Dummy />
            </StandardWrapper>
          ) : <Navigate to={Paths.auth.login} />
      )}
        path={Paths.base}
      />
    </Routes>
  );
}
