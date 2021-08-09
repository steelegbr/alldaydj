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
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
} from '@material-ui/core';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { CartSearchResults } from 'api/models/Search';
import CartSearchContext, { CartSearch } from 'components/context/CartSearchContext';
import Paths from 'routing/Paths';
import LibraryTableRow from 'pages/Library/LibraryTableRow';

interface LibraryTableProps {
    results: CartSearchResults
}

const LibraryTable = ({ results }: LibraryTableProps): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const history = useHistory();

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
        page: `${newPage + 1}`,
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
    <>
      <TableContainer component={Paper}>
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
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={results.count}
        onChangeRowsPerPage={changeResultsPerPage}
        onPageChange={changePage}
        page={page - 1}
        rowsPerPage={resultsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </>
  );
};

export default LibraryTable;
