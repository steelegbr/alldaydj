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

import { Cart } from 'api/models/Cart';
import React from 'react';

export interface CartEditorContextType {
    cart?: Cart,
    file?: File,
    setCart: React.Dispatch<React.SetStateAction<Cart | undefined>>;
    setFile: React.Dispatch<React.SetStateAction<File | undefined>>;
    clearCart: () => void;
    clearFile: () => void;
}

const noOp = () => {
  // Do nothing
};

export const CartEditorContext = React.createContext<CartEditorContextType>(
  {
    cart: undefined,
    setCart: noOp,
    setFile: noOp,
    clearCart: noOp,
    clearFile: noOp,
  },
);

export interface CartEditorProviderProps {
    children: React.ReactElement;
}

export const CartEditorProvider = ({ children }: CartEditorProviderProps): React.ReactElement => {
  const [cart, setCart] = React.useState<Cart>();
  const [file, setFile] = React.useState<File>();

  const clearCart = () => {
    setCart(undefined);
  };

  const clearFile = () => {
    setFile(undefined);
  };

  return (
    <CartEditorContext.Provider value={{
      cart, setCart, clearCart, file, setFile, clearFile,
    }}
    >
      {children}
    </CartEditorContext.Provider>
  );
};
