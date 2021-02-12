import {
  Button,
  createStyles,
  FormControl, Input, InputAdornment, InputLabel, makeStyles,
} from '@material-ui/core';
import { Search } from '@material-ui/icons';
import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import Paths from '../../routing/Paths';

type SearchConditionFields = 'advanced' | 'search';

type SearchConditions = Record<SearchConditionFields, string>;

const useStyles = makeStyles(() => createStyles({
  searchButton: {
    marginLeft: '20px',
  },
}));

const LibrarySearch = (): React.ReactElement => {
  const query = new URLSearchParams(useLocation().search);
  const history = useHistory();
  const [conditions, setConditions] = React.useState<SearchConditions>(
    {
      advanced: query.get('advanced') || 'false',
      search: query.get('search') || '',
    },
  );
  const classes = useStyles();

  const updateConditions = (newConditions: SearchConditions) => {
    setConditions(newConditions);
  };

  const updateSeachTerm = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...conditions,
      search: event.target.value,
    });
  };

  const performSearch = (event: React.SyntheticEvent) => {
    event.preventDefault();
    history.push({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(conditions).toString()}`,
    });
  };

  return (
    <form data-test="form-library-search" onSubmit={performSearch}>
      <FormControl>
        <InputLabel htmlFor="search">
          Search:
        </InputLabel>
        <Input
          data-test="input-search"
          id="search"
          name="search"
          onChange={updateSeachTerm}
          startAdornment={(
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          )}
          value={conditions.search}
        />
      </FormControl>
      <Button className={classes.searchButton} color="primary" type="submit" variant="contained">
        Search
      </Button>
    </form>
  );
};

export default LibrarySearch;
