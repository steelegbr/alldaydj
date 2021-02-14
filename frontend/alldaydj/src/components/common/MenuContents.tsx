import {
  createStyles, Divider, List, ListItem, ListItemIcon, ListItemText, makeStyles, Theme,
} from '@material-ui/core';
import { ExitToApp, LibraryMusic } from '@material-ui/icons';
import React from 'react';
import { useHistory } from 'react-router-dom';
import Paths from '../../routing/Paths';

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar,
}));

const MenuContents = (): React.ReactElement => {
  const classes = useStyles();
  const history = useHistory();

  const menuItemLibrary = () => (
    <ListItem
      button
      key="Music Library"
      onClick={(event) => {
        event.preventDefault();
        history.push(Paths.library.search);
      }}
    >
      <ListItemIcon>
        <LibraryMusic />
      </ListItemIcon>
      <ListItemText primary="Music Library" />
    </ListItem>
  );

  const menuItemLogout = () => (
    <ListItem
      button
      data-test="button-logout"
      key="Log Out"
      onClick={(event) => {
        event.preventDefault();
        history.push(Paths.auth.logout);
      }}
    >
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
