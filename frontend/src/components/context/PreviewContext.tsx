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

export type PreviewCartId = string | undefined;

export interface PreviewContextType {
    cartId: PreviewCartId;
    setCartId: React.Dispatch<React.SetStateAction<PreviewCartId>>;
    clearCart: Function;
}

const noOp = () => {
  // Do nothing
};

export const PreviewContext = React.createContext<PreviewContextType>({
  cartId: undefined,
  setCartId: noOp,
  clearCart: noOp,
});

export interface PreviewProviderProps {
    children: React.ReactElement;
}

export const PreviewProvider = ({ children }: PreviewProviderProps): React.ReactElement => {
  const [cartId, setCartId] = React.useState<PreviewCartId>();
  const clearCart = () => {
    setCartId(undefined);
  };

  return (
    <PreviewContext.Provider value={{ cartId, setCartId, clearCart }}>
      {children}
    </PreviewContext.Provider>
  );
};
