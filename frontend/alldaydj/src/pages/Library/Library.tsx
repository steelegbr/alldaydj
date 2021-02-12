import { Typography } from '@material-ui/core';
import React from 'react';
import LibrarySearch from './LibrarySearch';

const Library = (): React.ReactElement => (
  <>
    <Typography variant="h1">
      Music Library
    </Typography>
    <LibrarySearch />
  </>
);

export default Library;
