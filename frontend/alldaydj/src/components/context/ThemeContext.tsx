import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import React from 'react';
import { getLogger } from 'services/LoggingService';

export interface ThemeSettings {
  darkMode: boolean;
}

export interface ThemeContextProps {
  themeSettings: ThemeSettings;
  setThemeSettings: React.Dispatch<React.SetStateAction<ThemeSettings>>;
}

export const ThemeContext = React.createContext<undefined | ThemeContextProps>(undefined);

interface ThemeProviderProps {
  children: React.ReactElement;
}

export function ThemeProvider({ children }: ThemeProviderProps): React.ReactElement {
  const logger = getLogger();
  const darkMode = localStorage.getItem('darkMode') === 'true';
  logger.info(`Dark mode setting from local storage: ${darkMode}.`);

  const [themeSettings, setThemeSettings] = React.useState<ThemeSettings>({
    darkMode,
  });

  const theme = createMuiTheme({
    palette: {
      type: themeSettings.darkMode ? 'dark' : 'light',
      primary: {
        light: '#e1ffb1',
        main: '#aed581',
        dark: '#7da453',
        contrastText: '#000000',
      },
      secondary: {
        light: '#efdcd5',
        main: '#bcaaa4',
        dark: '#8c7b75',
        contrastText: '#000000',
      },
    },
  });

  localStorage.setItem('darkMode', themeSettings.darkMode ? 'true' : 'false');
  logger.info(`Set dark mode to ${themeSettings.darkMode} in local storage.`);

  return (
    <ThemeContext.Provider value={{ themeSettings, setThemeSettings }}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
}
