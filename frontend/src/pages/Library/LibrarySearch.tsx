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
  Button,
  TextField, Grid, InputAdornment,
} from '@mui/material';
import { Add, Search } from '@mui/icons-material';
import createStyles from '@mui/styles/createStyles';
import makeStyles from '@mui/styles/makeStyles';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CartSearchConditions } from 'api/models/Search';
import LoadingButton from 'components/common/LoadingButton';
import CartSearchContext, { CartSearchStatus } from 'components/context/CartSearchContext';
import Paths from 'routing/Paths';

const useStyles = makeStyles(() => createStyles({
  searchButton: {
    marginRight: 10,
    marginBottom: 10,
  },
}));

const LibrarySearch = (): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const navigate = useNavigate();
  const classes = useStyles();

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

    navigate({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(newConditions).toString()}`,
    });
  };

  const newCart = () => {
    navigate(Paths.cart);
  };

  return (
    <form data-test="form-library-search" onSubmit={performSearch}>
      <TextField
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
        data-test="input-search"
        fullWidth
        id="search"
        label="Search:"
        margin="normal"
        name="search"
        onChange={updateSearchTerm}
        value={search.conditions.search}
      />
      <Grid container>
        <Grid item>
          <LoadingButton className={classes.searchButton} color="primary" data-test="button-search" loading={search.status === 'Searching'} type="submit" variant="contained">
            Search
          </LoadingButton>
        </Grid>
        <Grid item>
          <Button
            data-test="button-add"
            onClick={newCart}
            variant="contained"
          >
            <Add />
            Add New
          </Button>
        </Grid>
      </Grid>

    </form>
  );
};

export default LibrarySearch;
