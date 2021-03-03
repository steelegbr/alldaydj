import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import Layout from 'pages/Layout';
import AuthenticationProvider from 'components/context/AuthenticationContext';
import { ThemeProvider } from 'components/context/ThemeContext';

function appWithBrowser() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}

function App(): React.ReactElement {
  return (
    <ThemeProvider>
      <AuthenticationProvider>
        {appWithBrowser()}
      </AuthenticationProvider>
    </ThemeProvider>
  );
}

export default App;
