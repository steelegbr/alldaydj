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

const LibraryTableRow = ({ result }: TableRowProps) => {
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
