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
  TableSortLabel,
} from '@mui/material';
import React from 'react';
import { useHistory } from 'react-router-dom';
import CartSearchContext, { CartSearch } from 'components/context/CartSearchContext';
import Paths from 'routing/Paths';
import LibraryTableRow from 'pages/Library/LibraryTableRow';
import { Paginated } from 'api/models/Pagination';
import { Cart } from 'api/models/Cart';
import { CartSearchOrderBy } from 'api/models/Search';

const ORDER_BY_ASC = [CartSearchOrderBy.Artist, CartSearchOrderBy.Label, CartSearchOrderBy.Title];
const ORDER_BY_LABEL = [CartSearchOrderBy.Label, CartSearchOrderBy.LabelDesc];
const ORDER_BY_ARTIST = [CartSearchOrderBy.Artist, CartSearchOrderBy.ArtistDesc];
const ORDER_BY_TITLE = [CartSearchOrderBy.Title, CartSearchOrderBy.TitleDesc];

interface LibraryTableProps {
    results: Paginated<Cart>
}

const LibraryTable = ({ results }: LibraryTableProps): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const history = useHistory();

  const page = Number.parseInt(search.conditions.page, 10);
  const resultsPerPage = Number.parseInt(search.conditions.resultsPerPage, 10);

  const updateSearch = React.useCallback(
    (newSearch: CartSearch) => {
      setSearch(newSearch);
      history.push({
        pathname: Paths.library.search,
        search: `?${new URLSearchParams(newSearch.conditions).toString()}`,
      });
    },
    [history, setSearch],
  );

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

  const orderByIsActive = React.useCallback(
    (permittedConditions: CartSearchOrderBy[]) => permittedConditions.some(
      (value) => value === search.conditions.order,
    ),
    [search.conditions.order],
  );

  const orderByDirection = React.useCallback(
    (permittedConditions: CartSearchOrderBy[]) => {
      if (orderByIsActive(permittedConditions)) {
        return ORDER_BY_ASC.some((value) => value === search.conditions.order) ? 'asc' : 'desc';
      }
      return 'asc';
    },
    [orderByIsActive, search.conditions.order],
  );

  const setOrderBy = React.useCallback(
    (permittedConditions: CartSearchOrderBy[]) => {
      if (orderByIsActive(permittedConditions)) {
        const otherValues = permittedConditions.filter(
          (value) => value !== search.conditions.order,
        );
        updateSearch({
          conditions: {
            ...search.conditions,
            order: otherValues[0],
          },
          status: 'ReadyToSearch',
        });
      } else {
        updateSearch({
          conditions: {
            ...search.conditions,
            order: permittedConditions[0],
          },
          status: 'ReadyToSearch',
        });
      }
    },
    [orderByIsActive, search.conditions, updateSearch],
  );

  return (
    <>
      <TableContainer component={Paper}>
        <Table aria-label="library search results">
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell>
                <TableSortLabel
                  active={orderByIsActive(ORDER_BY_LABEL)}
                  direction={orderByDirection(ORDER_BY_LABEL)}
                  onClick={() => setOrderBy(ORDER_BY_LABEL)}
                >
                  Label
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderByIsActive(ORDER_BY_ARTIST)}
                  direction={orderByDirection(ORDER_BY_ARTIST)}
                  onClick={() => setOrderBy(ORDER_BY_ARTIST)}
                >
                  Artist
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderByIsActive(ORDER_BY_TITLE)}
                  direction={orderByDirection(ORDER_BY_TITLE)}
                  onClick={() => setOrderBy(ORDER_BY_TITLE)}
                >
                  Title
                </TableSortLabel>
              </TableCell>
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
        onPageChange={changePage}
        onRowsPerPageChange={changeResultsPerPage}
        page={page - 1}
        rowsPerPage={resultsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </>
  );
};

export default LibraryTable;
