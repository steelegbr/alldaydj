import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  createStyles,
  FormControl, Input, InputAdornment, InputLabel, makeStyles, Theme, Typography,
} from '@material-ui/core';
import { Person, Search, Toc } from '@material-ui/icons';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { CartSearchConditions } from '../../api/models/Search';
import LoadingButton from '../../components/common/LoadingButton';
import CartSearchContext, { CartSearchStatus } from '../../components/context/CartSearchContext';
import Paths from '../../routing/Paths';

const useStyles = makeStyles((theme: Theme) => createStyles({
  formLayout: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const LibrarySearch = (): React.ReactElement => {
  const { search, setSearch } = React.useContext(CartSearchContext);
  const history = useHistory();
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

  const updateArtist = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...search.conditions,
      artist: event.target.value,
    },
    search.status);
  };

  const updateTitle = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...search.conditions,
      title: event.target.value,
    },
    search.status);
  };

  const performSearch = (event: React.SyntheticEvent) => {
    event.preventDefault();

    if (search.status === 'Searching') {
      return;
    }

    updateConditions(
      search.conditions,
      'ReadyToSearch',
    );

    history.push({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(search.conditions).toString()}`,
    });
  };

  const toggleAdvanced = () => {
    const nextAdvancedState = !(search.conditions.advanced === 'true');
    updateConditions({
      ...search.conditions,
      advanced: nextAdvancedState ? 'true' : 'false',
    },
    search.status);
  };

  return (
    <form className={classes.formLayout} data-test="form-library-search" onSubmit={performSearch}>
      <FormControl>
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
      <Accordion expanded={search.conditions.advanced === 'true'} onChange={toggleAdvanced}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
        >
          <Typography>Advanced Search</Typography>
        </AccordionSummary>
        <AccordionDetails className={classes.formLayout}>
          <FormControl>
            <InputLabel htmlFor="artist">
              Artist:
            </InputLabel>
            <Input
              data-test="input-artist"
              id="artist"
              name="artist"
              onChange={updateArtist}
              startAdornment={(
                <InputAdornment position="start">
                  <Person />
                </InputAdornment>
          )}
              value={search.conditions.artist}
            />
          </FormControl>
          <FormControl>
            <InputLabel htmlFor="title">
              Title:
            </InputLabel>
            <Input
              data-test="input-title"
              id="title"
              name="title"
              onChange={updateTitle}
              startAdornment={(
                <InputAdornment position="start">
                  <Toc />
                </InputAdornment>
          )}
              value={search.conditions.title}
            />
          </FormControl>
        </AccordionDetails>
      </Accordion>
    </form>
  );
};

export default LibrarySearch;
