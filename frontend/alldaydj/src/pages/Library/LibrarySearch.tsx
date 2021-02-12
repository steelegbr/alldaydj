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
import Paths from '../../routing/Paths';

type SearchConditionFields = 'advanced' | 'search';

type SearchConditions = Record<SearchConditionFields, string>;

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
      <Accordion>
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
              startAdornment={(
                <InputAdornment position="start">
                  <Person />
                </InputAdornment>
          )}
              value={conditions.search}
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
              startAdornment={(
                <InputAdornment position="start">
                  <Toc />
                </InputAdornment>
          )}
              value={conditions.search}
            />
          </FormControl>
        </AccordionDetails>
      </Accordion>
    </form>
  );
};

export default LibrarySearch;
