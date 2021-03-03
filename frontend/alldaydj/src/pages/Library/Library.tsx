import { Snackbar, Typography } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
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
