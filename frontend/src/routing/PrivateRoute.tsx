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

/* eslint-disable react/jsx-props-no-spreading */

import React from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import { isAuthenticated } from 'services/AuthenticationService';
import { getLogger } from 'services/LoggingService';
import Paths from 'routing/Paths';

export default function PrivateRoute(props: RouteProps): React.ReactElement {
  const authenticationContext = React.useContext(AuthenticationContext);
  const authenticated = isAuthenticated(authenticationContext);

  if (authenticated) {
    return <Route {...props} />;
  }

  getLogger().warn('Attempt to access private route while not authenticated!');
  return (
    <Route {...props}>
      <Redirect to={Paths.auth.login} />
    </Route>
  );
}
