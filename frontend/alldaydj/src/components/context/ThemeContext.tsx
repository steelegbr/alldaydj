import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import React from 'react';

export interface ThemeSettings {
    darkMode: boolean
};

export interface ThemeContextProps {
    themeSettings: ThemeSettings,
    setThemeSettings: React.Dispatch<React.SetStateAction<ThemeSettings>>
}

export const ThemeContext = React.createContext<undefined | ThemeContextProps>(undefined);

interface ThemeProviderProps {
    children: JSX.Element
}

export const ThemeProvider =  ({ children }: ThemeProviderProps) => {
    const [themeSettings, setThemeSettings] = React.useState<ThemeSettings>({
        darkMode: false
    });

    const theme = createMuiTheme({
       palette: {
            type: themeSettings.darkMode ? "dark": "light"
       } 
    });

    return (
        <ThemeContext.Provider value={{ themeSettings, setThemeSettings }}>
            <MuiThemeProvider theme={theme}>
                {children}
            </MuiThemeProvider>
        </ThemeContext.Provider>
    );

}