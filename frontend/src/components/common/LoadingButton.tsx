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

/* eslint-disable react/jsx-props-no-spreading */

import {
  Box, Button, ButtonProps, CircularProgress,
} from '@mui/material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
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

const LoadingButton = (props : LoadingButtonProps & ButtonProps): React.ReactElement => {
  const { loading } = props;
  const classes = useStyles();

  return (
    <Box className={classes.wrapper}>
      <Button disabled={loading ? true : undefined} {...props} />
      {loading && (
        <CircularProgress className={classes.loadingSpinner} size={24} />
      )}
    </Box>
  );
};

export default LoadingButton;
