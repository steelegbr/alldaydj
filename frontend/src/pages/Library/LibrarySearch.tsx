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
  FormControl, Input, InputAdornment, InputLabel,
} from '@mui/material';
import { Search } from '@mui/icons-material';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { CartSearchConditions } from 'api/models/Search';
import LoadingButton from 'components/common/LoadingButton';
import CartSearchContext, { CartSearchStatus } from 'components/context/CartSearchContext';
import Paths from 'routing/Paths';

const LibrarySearch = (): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const history = useHistory();

  const updateConditions = (newConditions: CartSearchConditions, status: CartSearchStatus) => {
    setSearch({
      conditions: newConditions,
      status,
    });
  };

  const updateSearchTerm = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...search.conditions,
      search: event.target.value,
    },
    search.status);
  };

  const performSearch = (event: React.SyntheticEvent) => {
    event.preventDefault();

    if (search.status === 'Searching') {
      return;
    }

    const newConditions = {
      ...search.conditions,
      page: '1',
    };

    updateConditions(
      newConditions,
      'ReadyToSearch',
    );

    history.push({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(newConditions).toString()}`,
    });
  };

  return (
    <form data-test="form-library-search" onSubmit={performSearch}>
      <FormControl variant="standard">
        <InputLabel htmlFor="search">
          Search:
        </InputLabel>
        <Input
          data-test="input-search"
          id="search"
          name="search"
          onChange={updateSearchTerm}
          startAdornment={(
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          )}
          value={search.conditions.search}
        />
      </FormControl>
      <LoadingButton color="primary" data-test="button-search" loading={search.status === 'Searching'} type="submit" variant="contained">
        Search
      </LoadingButton>
    </form>
  );
};

export default LibrarySearch;
