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
  Button, Collapse, IconButton, TableCell, TableRow, makeStyles, createStyles, Box,
} from '@material-ui/core';
import {
  GetApp, KeyboardArrowDown, KeyboardArrowUp, PlayArrow,
} from '@material-ui/icons';
import React from 'react';
import { CartSearchResult } from 'api/models/Search';

const useStyles = makeStyles(() => createStyles({
  collapsedRow: {
    paddingBottom: 0,
    paddingTop: 0,
  },
  collapsedBox: {
    margin: 1,
  },
}));

interface TableRowProps {
    result: CartSearchResult
}

const LibraryTableRow = ({ result }: TableRowProps): React.ReactElement => {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  return (
    <>
      <TableRow>
        <TableCell>
          <IconButton aria-label="expand search result" data-test="result-expand" onClick={() => setOpen(!open)} size="small">
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
          </IconButton>
        </TableCell>
        <TableCell>{result.label}</TableCell>
        <TableCell>{result.artist}</TableCell>
        <TableCell>{result.title}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell className={classes.collapsedRow} colSpan={4}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box className={classes.collapsedBox}>
              <Button aria-controls="preview audio">
                <PlayArrow />
                {' '}
                Preview Cart
              </Button>
              <Button aria-controls="download compressed audio">
                <GetApp />
                {' '}
                Compressed (OGG)
              </Button>
              <Button aria-controls="download linear audio">
                <GetApp />
                {' '}
                Linear (WAV)
              </Button>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

export default LibraryTableRow;
