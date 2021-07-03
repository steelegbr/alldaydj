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

import React from 'react';
import { useLocation } from 'react-router-dom';
import { CartSearchConditions } from 'api/models/Search';
import { cartSearchContextFromQueryString } from 'services/SearchService';

export type CartSearchStatus = 'NotStarted' | 'ReadyToSearch' | 'Searching' | 'ResultsReturned' | 'Error';

export interface CartSearch {
    conditions: CartSearchConditions,
    status: CartSearchStatus
}

export interface CartSearchContextType {
    search: CartSearch,
    setSearch: React.Dispatch<React.SetStateAction<CartSearch>>
}

const noOp = () => {
  // Do nothing
};

const CartSearchContext = React.createContext<CartSearchContextType>({
  search: {
    conditions: {
      page: '1',
      resultsPerPage: '10',
      search: '',
    },
    status: 'NotStarted',
  },
  setSearch: noOp,
});

export interface CartSearchProviderProps {
    children: React.ReactElement;
  }

export const CartSearchProvider = ({ children }: CartSearchProviderProps): React.ReactElement => {
  const query = new URLSearchParams(useLocation().search);
  const [search, setSearch] = React.useState<CartSearch>(
    cartSearchContextFromQueryString(query),
  );

  return (
    <CartSearchContext.Provider value={{ search, setSearch }}>
      {children}
    </CartSearchContext.Provider>
  );
};
export default CartSearchContext;
