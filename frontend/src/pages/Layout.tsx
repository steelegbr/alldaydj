import {
  createStyles, CssBaseline, makeStyles, Theme,
} from '@material-ui/core';
import React from 'react';
import Menu from '../components/common/Menu';
import ApplicationRouter from '../routing/ApplicationRouter';

const useStyles = makeStyles((theme: Theme) => createStyles({
  toolbar: theme.mixins.toolbar,
}));

export default function Layout() : React.ReactElement {
  const classes = useStyles();

  return (
    <div>
      <CssBaseline />
      <Menu />
      <div className={classes.toolbar} />
      <ApplicationRouter />
    </div>
  );
}
