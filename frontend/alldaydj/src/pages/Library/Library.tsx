import { Snackbar, Typography } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import React, { useEffect } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import { CartSearchResults } from '../../api/models/Search';
import { cartSearch } from '../../api/requests/Search';
import { AuthenticationContext } from '../../components/context/AuthenticationContext';
import { paramsToSearchConditions } from '../../services/SearchService';
import LibrarySearch from './LibrarySearch';
import LibraryTable from './LibraryTable';

type SearchState = 'Idle' | 'Loading' | 'Error';

const Library = (): React.ReactElement => {
  const history = useHistory();
  const query = new URLSearchParams(useLocation().search);
  const searchConditions = paramsToSearchConditions(query);
  const [
    searchResults,
    setSearchResults,
  ] = React.useState<CartSearchResults | undefined>(undefined);
  const [state, setState] = React.useState<SearchState>('Idle');
  const [errorMessage, setErrorMessage] = React.useState<string>('');
  const authenticatonContext = React.useContext(AuthenticationContext);
  const accessToken = authenticatonContext?.authenticationStatus.accessToken;

  useEffect(() => {
    history.listen(() => {
      if (accessToken) {
        setState('Loading');
        cartSearch(searchConditions, 1, 10, accessToken).then(
          (results) => {
            setState('Idle');
            setSearchResults(results.data);
          },
          (error) => {
            setState('Error');
            setErrorMessage(`Failed to load the search results. Reason: ${error}`);
          },
        );
      }
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Typography variant="h1">
        Music Library
      </Typography>
      <LibrarySearch />
      <Snackbar autoHideDuration={6000} data-test="box-error" open={state === 'Error'}>
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
