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
  makeStyles, Theme, createStyles, Box, Grid,
} from '@material-ui/core';
import React from 'react';

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar,
  bgImage: {
    backgroundImage: "url('/login_background.jpg')",
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundSize: 'cover',
    height: '100vh',
    width: '100vw',
    position: 'absolute',
    top: 0,
    left: 0,
  },
  loginBox: {
    paddingTop: 10,
  },
}));

// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface Props {}

export default function
AuthenticationWrapper({ children }: React.PropsWithChildren<Props>): React.ReactElement {
  const classes = useStyles();

  return (
    <Box className={classes.bgImage}>
      <Box className={classes.toolbar} />
      <Grid className={classes.loginBox} container justify="center">
        <Grid item md={4} xs={12}>
          <div role="main">
            {children}
          </div>
        </Grid>
      </Grid>
    </Box>
  );
}
