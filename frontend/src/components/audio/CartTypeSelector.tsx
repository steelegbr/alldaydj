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
  FormControl, InputLabel, ListItemIcon, MenuItem, Select, SelectChangeEvent,
} from '@mui/material';
import { CartType } from 'api/models/Cart';
import { getCartTypes } from 'api/requests/Cart';
import { AuthenticationContext } from 'components/context/AuthenticationContext';
import React from 'react';
import { getLogger } from 'services/LoggingService';

interface CartTypeSelectorProps {
    selectedType: string,
    setSelectedType: (newType: string) => void
}

const CartTypeSelector = (
  { selectedType, setSelectedType }: CartTypeSelectorProps,
): React.ReactElement => {
  const [cartTypes, setCartTypes] = React.useState<CartType[]>([]);
  const authenticatonContext = React.useContext(AuthenticationContext);
  const token = authenticatonContext?.authenticationStatus.accessToken;

  React.useEffect(
    () => {
      if (token) {
        getLogger().info('Downloading cart types.');
        getCartTypes(token).then(
          (loadedCartTypes: CartType[]) => {
            setCartTypes(loadedCartTypes);
          },
          (error) => {
            getLogger().error(`Something went wrong updating the cart types: ${error}`);
            setCartTypes([]);
          },
        );
      }
    },
    [token],
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
      <Select id="cart-type" labelId="cart-type" onChange={updateTypeSelection} value={selectedType}>
        {cartTypes.map((cartType) => (
          <MenuItem value={cartType.name}>
            <ListItemIcon>
              <Stop style={{ fill: cartType.colour }} />
            </ListItemIcon>
            {cartType.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default CartTypeSelector;
