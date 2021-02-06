import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Hidden,
  Drawer,
  useTheme,
  Grid,
  makeStyles,
  createStyles,
  Theme,
} from '@material-ui/core';
import { Brightness4, Brightness7 } from '@material-ui/icons';
import MenuIcon from '@material-ui/icons/Menu';
import React from 'react';
import { isAuthenticated } from '../../services/AuthenticationService';
import { AuthenticationContext } from '../context/AuthenticationContext';
import { ThemeContext } from '../context/ThemeContext';
import MenuContents from './MenuContents';

const drawerWidth = 240;

const useStyles = makeStyles((theme: Theme) => createStyles({
  root: {
    display: 'flex',
  },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: drawerWidth,
      flexShrink: 0,
    },
  },
  appBar: {
    marginLeft: drawerWidth,
    zIndex: theme.zIndex.drawer + 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
    [theme.breakpoints.up('sm')]: {
      display: 'none',
    },
  },
  toolbar: theme.mixins.toolbar,
  drawerPaper: {
    width: drawerWidth,
  },
}));

const Menu = (): React.ReactElement => {
  const theme = useTheme();
  const [menuOpen, setMenuOpen] = React.useState(false);
  const themeContext = React.useContext(ThemeContext);
  const authenticationContext = React.useContext(AuthenticationContext);
  const authenticated = isAuthenticated(authenticationContext, true);

  const classes = useStyles();
  const container = window.document.body;
  const darkMode = themeContext?.themeSettings.darkMode;

  function handleMenuToggle() {
    setMenuOpen(!menuOpen);
  }

  function handleDarkModeToggle() {
    if (themeContext) {
      const newThemeSettings = {
        ...themeContext.themeSettings,
        darkMode: !darkMode,
      };
      themeContext.setThemeSettings(newThemeSettings);
    }
  }

  function menuToggleButton() {
    return (
      <Grid item>
        {authenticated && (
          <IconButton
            aria-label="open menu"
            className={classes.menuButton}
            color="inherit"
            data-test="button-menu-toggle"
            edge="start"
            onClick={handleMenuToggle}
          >
            <MenuIcon />
          </IconButton>
        )}
      </Grid>
    );
  }

  function menuHeader() {
    return (
      <Grid item>
        <Typography noWrap variant="h6">
          AllDay DJ
        </Typography>
      </Grid>
    );
  }

  function menuDarkModeToggle() {
    return (
      <Grid item>
        <IconButton
          arial-label="toggle light / dark mode"
          color="inherit"
          edge="end"
          onClick={handleDarkModeToggle}
        >
          {darkMode ? <Brightness4 /> : <Brightness7 />}
        </IconButton>
      </Grid>
    );
  }

  function headerToolbar() {
    return (
      <Toolbar>
        <Grid alignItems="center" container justify="space-between">
          {menuToggleButton()}
          {menuHeader()}
          {menuDarkModeToggle()}
        </Grid>
      </Toolbar>
    );
  }

  function drawerWide() {
    return (
      <Hidden implementation="css" smUp>
        <Drawer
          ModalProps={{
            keepMounted: true,
          }}
          anchor={theme.direction === 'rtl' ? 'right' : 'left'}
          classes={{
            paper: classes.drawerPaper,
          }}
          container={container}
          onClose={handleMenuToggle}
          open={menuOpen}
          variant="persistent"
        >
          <MenuContents />
        </Drawer>
      </Hidden>
    );
  }

  function drawerMobile() {
    return (
      <Hidden implementation="css" xsDown>
        <Drawer
          classes={{
            paper: classes.drawerPaper,
          }}
          open
          variant="permanent"
        >
          <MenuContents />
        </Drawer>
      </Hidden>
    );
  }

  return (
    <div>
      <AppBar className={classes.appBar} position="fixed">
        {headerToolbar()}
      </AppBar>
      {authenticated && (
        <nav aria-label="main menu" className={classes.drawer}>
          {drawerWide()}
          {drawerMobile()}
        </nav>
      )}
    </div>
  );
};

export default Menu;
