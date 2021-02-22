import React from 'react';
import { useLocation } from 'react-router-dom';
import { CartSearchConditions } from '../../api/models/Search';
import { cartSearchContextFromQueryString } from '../../services/SearchService';

export type CartSearchStatus = 'NotStarted' | 'ReadyToSearch' | 'Searching' | 'ResultsReturned' | 'Error';

export interface CartSearch {
    conditions: CartSearchConditions,
    status: CartSearchStatus
}

export interface CartSearchContextType {
    search: CartSearch,
    setSearch: React.Dispatch<React.SetStateAction<CartSearch>>
}

const CartSearchContext = React.createContext<CartSearchContextType>({
  search: {
    conditions: {
      advanced: 'false',
      artist: '',
      page: '1',
      resultsPerPage: '10',
      search: '',
      title: '',
    },
    status: 'NotStarted',
  },
  setSearch: () => {},
});

export interface CartSearchProviderProps {
    children: React.ReactElement;
  }

export const CartSearchProvider = ({ children }: CartSearchProviderProps) => {
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
