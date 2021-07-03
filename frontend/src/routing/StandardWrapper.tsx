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
import { createStyles, makeStyles, Theme } from '@material-ui/core';

const drawerWidth = 240;

const useStyles = makeStyles((theme: Theme) => createStyles({
  content: {
    [theme.breakpoints.up('sm')]: {
      left: drawerWidth,
      width: `calc(100vw - ${drawerWidth}px)`,
      position: 'relative',
    },
    padding: 10,
  },
}));

// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface Props {}

const StandardWrapper = ({ children }: React.PropsWithChildren<Props>) : React.ReactElement => {
  const classes = useStyles();
  return (
    <div className={classes.content}>
      {children}
    </div>
  );
};

export default StandardWrapper;
