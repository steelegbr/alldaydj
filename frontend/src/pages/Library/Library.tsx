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

import { Alert, Snackbar, Typography } from '@mui/material';
import React, { useEffect } from 'react';
import { CartSearchResults } from 'api/models/Search';
import { cartSearch } from 'api/requests/Search';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import CartSearchContext from 'components/context/CartSearchContext';
import LibrarySearch from 'pages/Library/LibrarySearch';
import LibraryTable from 'pages/Library/LibraryTable';

const Library = (): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const [
    searchResults,
    setSearchResults,
  ] = React.useState<CartSearchResults | undefined>(undefined);
  const [errorMessage, setErrorMessage] = React.useState<string>('');
  const authenticatonContext = React.useContext(AuthenticationContext);
  const accessToken = authenticatonContext?.authenticationStatus.accessToken;

  useEffect(() => {
    if (accessToken && search.status === 'ReadyToSearch') {
      setSearch({
        conditions: {
          ...search.conditions,
        },
        status: 'Searching',
      });
      cartSearch(search.conditions, accessToken).then(
        (results) => {
          setSearch({
            conditions: {
              ...search.conditions,
            },
            status: 'ResultsReturned',
          });
          setSearchResults(results.data);
        },
        (error) => {
          setSearch({
            conditions: {
              ...search.conditions,
            },
            status: 'Error',
          });
          setErrorMessage(`Failed to load the search results. Reason: ${error}`);
        },
      );
    }
  }, [search, setSearch, accessToken]);

  return (
    <>
      <Typography variant="h1">
        Music Library
      </Typography>
      <LibrarySearch />
      <Snackbar autoHideDuration={6000} data-test="box-error" open={search.status === 'Error'}>
        <Alert elevation={6} severity="error" variant="filled">
          {errorMessage}
        </Alert>
      </Snackbar>
      {searchResults && (
      <LibraryTable results={searchResults} />
      )}

    </>
  );
};

export default Library;
