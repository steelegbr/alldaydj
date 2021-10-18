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
import { BrowserRouter } from 'react-router-dom';
import Layout from 'pages/Layout';
import AuthenticationProvider from 'components/context/AuthenticationContext';
import { AppThemeProvider } from 'components/context/ThemeContext';
import { PreviewProvider } from 'components/context/PreviewContext';
import { StyledEngineProvider, Theme } from '@mui/material/styles';

declare module '@mui/styles/defaultTheme' {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  // eslint-disable-next-line no-unused-vars
  // skipcq: JS-0322
  interface DefaultTheme extends Theme {}
}

function App(): React.ReactElement {
  return (
    <StyledEngineProvider injectFirst>
      <AppThemeProvider>
        <AuthenticationProvider>
          <PreviewProvider>
            <BrowserRouter>
              <Layout />
            </BrowserRouter>
          </PreviewProvider>
        </AuthenticationProvider>
      </AppThemeProvider>
    </StyledEngineProvider>
  );
}

export default App;
