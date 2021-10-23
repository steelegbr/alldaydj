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
  Autocomplete, TextField,
} from '@mui/material';
import { Tag } from 'api/models/Cart';
import { getTags } from 'api/requests/Cart';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import React, { SyntheticEvent } from 'react';
import { getLogger } from 'services/LoggingService';

interface TagChipsProps {
    selectedTags: string[],
    setSelectedTags: (tags: string[]) => void
}

const TagChips = (
  { selectedTags, setSelectedTags }: TagChipsProps,
): React.ReactElement => {
  const [availableTags, setAvailableTags] = React.useState<string[]>([]);
  const authenticatonContext = React.useContext(AuthenticationContext);
  const token = authenticatonContext?.authenticationStatus.accessToken;

  React.useEffect(
    () => {
      if (token) {
        getLogger().info('Obtaining possible tags.');
        getTags(token).then(
          (tags: Tag[]) => {
            const mappedTags = tags.map((tag) => tag.tag);
            setAvailableTags(mappedTags);
          },
          (error) => {
            getLogger().error(`Failed to get tags: ${error}`);
          },
        );
      }
    },
    [token],
  );

  //   const deleteTag = React.useCallback(
  //     (tag: string) => {
  //       const updatedTags = selectedTags.filter((currentTag) => currentTag !== tag);
  //       setSelectedTags(updatedTags);
  //     },
  //     [selectedTags, setSelectedTags],
  //   );

  const setTags = React.useCallback(
    (event: SyntheticEvent<Element, Event>, tags: string[]) => {
      setSelectedTags(tags);
    },
    [setSelectedTags],
  );

  const filteredAvailableTags = availableTags.filter((tag) => !selectedTags.includes(tag));

  return (
    <Autocomplete
      disablePortal
      id="cart-tags"
      multiple
      onChange={setTags}
      options={filteredAvailableTags}
      renderInput={(params) => (
        <TextField
          margin="normal"
          placeholder="Add a tag"
            // eslint-disable-next-line react/jsx-props-no-spreading
          {...params}
          label="Tags:"
          variant="standard"
        />
      )}
      value={selectedTags}
    />
  );
};

export default TagChips;
