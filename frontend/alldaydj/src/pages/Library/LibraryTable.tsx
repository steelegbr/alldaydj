import {
  Paper, Table, TableBody, TableCell, TableContainer, TableFooter, TableHead, TableRow,
} from '@material-ui/core';
import React from 'react';
import { CartSearchResults } from '../../api/models/Search';
import LibraryTableRow from './LibraryTableRow';

interface LibraryTableProps {
    results: CartSearchResults
}

const LibraryTable = ({ results }: LibraryTableProps) => (
  <TableContainer component={Paper}>
    <Table aria-label="library search results" size="small">
      <TableHead>
        <TableRow>
          <TableCell>Label</TableCell>
          <TableCell>Artist</TableCell>
          <TableCell>Title</TableCell>
          <TableCell>Download</TableCell>
          <TableCell>Preview</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {results.results.map((result) => (<LibraryTableRow result={result} />))}
      </TableBody>
      <TableFooter>
        {results.count}
        {' '}
        search result(s).
      </TableFooter>
    </Table>
  </TableContainer>
);

export default LibraryTable;
