import {
  createStyles,
  makeStyles,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableFooter,
  TableHead,
  TablePagination,
  TableRow,
} from '@material-ui/core';
import React from 'react';
import { CartSearchResults } from '../../api/models/Search';
import LibraryTableRow from './LibraryTableRow';

const useStyles = makeStyles(() => createStyles({
  searchTableContainer: {
    tableLayout: 'fixed',
  },
}));

interface LibraryTableProps {
    results: CartSearchResults
}

const LibraryTable = ({ results }: LibraryTableProps) => {
  const classes = useStyles();

  return (
    <TableContainer className={classes.searchTableContainer} component={Paper}>
      <Table aria-label="library search results">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Label</TableCell>
            <TableCell>Artist</TableCell>
            <TableCell>Title</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.results.map((result) => (<LibraryTableRow key={result.id} result={result} />))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination
              colSpan={4}
              component="div"
              count={results.count}
              onChangePage={() => {}}
              onChangeRowsPerPage={() => {}}
              page={0}
              rowsPerPage={10}
              rowsPerPageOptions={[5, 10, 25]}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  );
};

export default LibraryTable;
