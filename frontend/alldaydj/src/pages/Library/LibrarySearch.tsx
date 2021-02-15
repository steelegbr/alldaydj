import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Button,
  createStyles,
  FormControl, Input, InputAdornment, InputLabel, makeStyles, Theme, Typography,
} from '@material-ui/core';
import { Person, Search, Toc } from '@material-ui/icons';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import { SearchConditions } from '../../api/models/Search';
import Paths from '../../routing/Paths';
import { paramsToSearchConditions } from '../../services/SearchService';

const useStyles = makeStyles((theme: Theme) => createStyles({
  formLayout: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const LibrarySearch = (): React.ReactElement => {
  const query = new URLSearchParams(useLocation().search);
  const history = useHistory();
  const [conditions, setConditions] = React.useState<SearchConditions>(
    paramsToSearchConditions(query),
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

  const updateArtist = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...conditions,
      artist: event.target.value,
    });
  };

  const updateTitle = (event: React.ChangeEvent<HTMLTextAreaElement|HTMLInputElement>) => {
    event.preventDefault();
    updateConditions({
      ...conditions,
      title: event.target.value,
    });
  };

  const performSearch = (event: React.SyntheticEvent) => {
    event.preventDefault();
    history.push({
      pathname: Paths.library.search,
      search: `?${new URLSearchParams(conditions).toString()}`,
    });
  };

  const toggleAdvanced = () => {
    const nextAdvancedState = !(conditions.advanced === 'true');
    updateConditions({
      ...conditions,
      advanced: nextAdvancedState ? 'true' : 'false',
    });
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
          onChange={updateSeachTerm}
          startAdornment={(
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          )}
          value={conditions.search}
        />
      </FormControl>
      <Button color="primary" type="submit" variant="contained">
        Search
      </Button>
      <Accordion expanded={conditions.advanced === 'true'} onChange={toggleAdvanced}>
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
              value={conditions.artist}
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
              value={conditions.title}
            />
          </FormControl>
        </AccordionDetails>
      </Accordion>
    </form>
  );
};

export default LibrarySearch;
