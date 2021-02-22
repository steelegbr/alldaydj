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
import { useHistory } from 'react-router-dom';
import { CartSearchResults } from '../../api/models/Search';
import CartSearchContext, { CartSearch } from '../../components/context/CartSearchContext';
import Paths from '../../routing/Paths';
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
  const { search, setSearch } = React.useContext(CartSearchContext);
  const history = useHistory();
  const classes = useStyles();

  const page = Number.parseInt(search.conditions.page, 10);
  const resultsPerPage = Number.parseInt(search.conditions.resultsPerPage, 10);

  const updateSearch = (newSearch: CartSearch) => {
    setSearch(newSearch);
    history.push({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(newSearch.conditions).toString()}`,
    });
  };

  const changePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    updateSearch({
      conditions: {
        ...search.conditions,
        page: `${newPage}`,
      },
      status: 'ReadyToSearch',
    });
  };

  const changeResultsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    updateSearch({
      conditions: {
        ...search.conditions,
        page: '1',
        resultsPerPage: event.target.value,
      },
      status: 'ReadyToSearch',
    });
  };

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
              component="div"
              count={results.count}
              onChangePage={changePage}
              onChangeRowsPerPage={changeResultsPerPage}
              page={page - 1}
              rowsPerPage={resultsPerPage}
              rowsPerPageOptions={[5, 10, 25]}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  );
};

export default LibraryTable;
