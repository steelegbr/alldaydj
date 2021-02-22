/* eslint-disable react/jsx-props-no-spreading */
import {
  Box, Button, ButtonProps, CircularProgress, createStyles, makeStyles,
} from '@material-ui/core';
import React from 'react';

const useStyles = makeStyles(() => createStyles({
  wrapper: {
    position: 'relative',
  },
  loadingSpinner: {
    position: 'absolute',
    left: '50%',
    top: '50%',
    marginLeft: -12,
    marginTop: -12,
  },
}));

interface LoadingButtonProps {
    loading: boolean
}

const LoadingButton = (props : LoadingButtonProps & ButtonProps) => {
  const { loading } = props;
  const classes = useStyles();

  return (
    <Box className={classes.wrapper}>
      <Button disabled={loading} {...props} />
      {loading && (
        <CircularProgress className={classes.loadingSpinner} size={24} />
      )}
    </Box>
  );
};

export default LoadingButton;
