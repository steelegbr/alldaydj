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
  Divider, List, ListItemButton, ListItemIcon, ListItemText,
} from '@mui/material';
import makeStyles from '@mui/styles/makeStyles';
import createStyles from '@mui/styles/createStyles';
import { Theme } from '@mui/material/styles';
import { ExitToApp, LibraryMusic } from '@mui/icons-material';
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
    <ListItemButton
      aria-posinset={1}
      aria-setsize={1}
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
    </ListItemButton>
  );

  const menuItemLogout = () => (
    <ListItemButton
      aria-posinset={1}
      aria-setsize={1}
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
    </ListItemButton>
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
