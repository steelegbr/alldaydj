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

import {
  createStyles, Divider, List, ListItem, ListItemIcon, ListItemText, makeStyles, Theme,
} from '@material-ui/core';
import { ExitToApp, LibraryMusic } from '@material-ui/icons';
import React from 'react';
import { useHistory } from 'react-router-dom';
import Paths from 'routing/Paths';

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar,
}));

const MenuContents = (): React.ReactElement => {
  const classes = useStyles();
  const history = useHistory();

  const menuItemLibrary = () => (
    <ListItem
      button
      data-test="button-library"
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
