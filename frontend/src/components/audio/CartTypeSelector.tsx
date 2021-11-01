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

import { Stop } from '@mui/icons-material';
import {
  FormControl, FormHelperText, InputLabel, ListItemIcon, MenuItem, Select, SelectChangeEvent,
} from '@mui/material';
import { CartType } from 'api/models/Cart';
import { getCartTypes } from 'api/requests/Cart';
import React from 'react';
import { getLogger } from 'services/LoggingService';

interface CartTypeSelectorProps {
    selectedType: string,
    setSelectedType: (newType: string) => void,
    selectionError: boolean
}

const CartTypeSelector = (
  { selectedType, setSelectedType, selectionError }: CartTypeSelectorProps,
): React.ReactElement => {
  const [cartTypes, setCartTypes] = React.useState<CartType[]>([]);

  React.useEffect(
    () => {
      getLogger().info('Downloading cart types.');
      getCartTypes().then(
        (loadedCartTypes: CartType[]) => {
          setCartTypes(loadedCartTypes);
        },
        (error) => {
          getLogger().error(`Something went wrong updating the cart types: ${error}`);
          setCartTypes([]);
        },
      );
    },
    [],
  );

  const updateTypeSelection = React.useCallback(
    (event: SelectChangeEvent<string>) => {
      if (cartTypes) {
        setSelectedType(event.target.value);
      }
    },
    [cartTypes, setSelectedType],
  );

  return (
    <FormControl fullWidth variant="standard">
      <InputLabel htmlFor="cart-type">Type:</InputLabel>
      <Select data-test="select-type" id="cart-type" labelId="cart-type" onChange={updateTypeSelection} value={selectedType}>
        {cartTypes.map((cartType) => (
          <MenuItem value={cartType.name}>
            <ListItemIcon>
              <Stop style={{ fill: cartType.colour }} />
            </ListItemIcon>
            {cartType.name}
          </MenuItem>
        ))}
      </Select>
      {selectionError && (
        <FormHelperText error>You must select a cart type.</FormHelperText>
      )}
    </FormControl>
  );
};

export default CartTypeSelector;
