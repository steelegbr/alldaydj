import {
  createStyles, Divider, List, ListItem, ListItemIcon, ListItemText, makeStyles, Theme,
} from '@material-ui/core';
import { ExitToApp, LibraryMusic } from '@material-ui/icons';
import React from 'react';
import { logOut } from '../../services/AuthenticationService';
import { AuthenticationContext } from '../context/AuthenticationContext';

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar,
}));

const MenuContents = (): React.ReactElement => {
  const classes = useStyles();
  const authenticationContext = React.useContext(AuthenticationContext);

  const doLogOut = () => {
    authenticationContext?.setAuthenticationStatus(logOut());
  };

  const menuItemLibrary = () => (
    <ListItem button key="Music Library">
      <ListItemIcon>
        <LibraryMusic />
      </ListItemIcon>
      <ListItemText primary="Music Library" />
    </ListItem>
  );

  const menuItemLogout = () => (
    <ListItem button data-test="button-logout" key="Log Out" onClick={doLogOut}>
      <ListItemIcon>
        <ExitToApp />
      </ListItemIcon>
      <ListItemText primary="Log Out" />
    </ListItem>
  );

  return (
    <div>
      <div className={classes.toolbar} />
      <Divider />
      <List>
        {menuItemLibrary()}
      </List>
      <Divider />
      <List>
        {menuItemLogout()}
      </List>
    </div>
  );
};

export default MenuContents;
