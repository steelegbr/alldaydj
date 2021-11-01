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
  FormControl, InputLabel, MenuItem, Select, SelectChangeEvent,
} from '@mui/material';
import { Sequencer, SequencerNext } from 'api/models/Cart';
import { getNextCartId, getSequencers } from 'api/requests/Cart';
import { AxiosResponse } from 'axios';
import React from 'react';
import { getLogger } from 'services/LoggingService';

interface CartSequencerProps {
    callback: (generated: string) => void
}

const CartSequencer = ({ callback }: CartSequencerProps): React.ReactElement => {
  const [sequencer, setSequencer] = React.useState<Sequencer>();
  const [sequencers, setSequencers] = React.useState<Sequencer[]>([]);
  const displayDropdown = sequencers && sequencers.length > 1;

  const handleGenerateClick = React.useCallback(
    () => {
      if (sequencer) {
        getNextCartId(sequencer).then(
          (response: AxiosResponse<SequencerNext>) => {
            if (response.status === 200) {
              callback(response.data.next);
            } else {
              getLogger().warn(`Got status code ${response.status} generating the next cart ID.`);
            }
          },
          (error) => {
            getLogger().error(`Got an error generating the next cart ID: ${error}`);
          },
        );
      }
    },
    [callback, sequencer],
  );

  const updateSequencerSelection = React.useCallback(
    (event: SelectChangeEvent<string>) => {
      const selectedSequencers = sequencers.filter((s) => s.name === event.target.value);
      if (selectedSequencers) {
        setSequencer(selectedSequencers[0]);
      }
    },
    [sequencers],
  );

  React.useEffect(
    () => {
      getLogger().info('Dowloading cart sequencer information.');
      getSequencers().then(
        (returnedSequencers) => {
          setSequencers(returnedSequencers);
          getLogger().info('Successfully downloaded sequencers.');
          if (returnedSequencers && returnedSequencers.length === 1) {
            setSequencer(returnedSequencers[0]);
            getLogger().info(`Set sequencer to default of ${returnedSequencers[0].name}`);
          }
        },
        (error) => {
          getLogger().error(`Failed to download the sequencers. Error: ${error}`);
        },
      );
    },
    [callback],
  );

  return (
    <>
      {displayDropdown && (
      <FormControl fullWidth variant="standard">
        <InputLabel htmlFor="select-sequencer">Generator:</InputLabel>
        <Select data-test="select-sequencer" id="cart-type" labelId="cart-type" onChange={updateSequencerSelection} value={sequencer?.name}>
          {sequencers.map((currentSequencer) => (
            <MenuItem value={currentSequencer.name}>
              {currentSequencer.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      )}
      <Button
        onClick={handleGenerateClick}
        variant="contained"
      >
        Generate
      </Button>
    </>
  );
};

export default CartSequencer;
