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

const StandardWrapper = ({ children }: React.PropsWithChildren<Props>) => {
  const classes = useStyles();
  return (
    <div className={classes.content}>
      {children}
    </div>
  );
};

export default StandardWrapper;
