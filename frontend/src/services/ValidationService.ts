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

const REGEX_LABEL = new RegExp('^[A-Za-z0-9]+');
const YEARS_IN_FUTURE = 100;
const CURRENT_YEAR = (new Date()).getFullYear();
export const MAX_PERMITTED_YEAR = CURRENT_YEAR + YEARS_IN_FUTURE;

export enum CartFields {
    Label = 'label',
    Year = 'year',
    Title = 'title',
    Type = 'type'
}

export const validateLabel = (label: string) => label && REGEX_LABEL.test(label);
export const validateYear = (year: number) => Number.isInteger(year)
 && year >= 0 && year <= (MAX_PERMITTED_YEAR);
export const validateNotBlank = (value: string) => !!(value);

export const validateCart = (cart: Cart | undefined): CartFields[] => {
  const errors: CartFields[] = [];

  if (cart) {
    if (!validateLabel(cart.label)) {
      errors.push(CartFields.Label);
    }

    if (!validateYear(cart.year)) {
      errors.push(CartFields.Year);
    }

    if (!validateNotBlank(cart.title)) {
      errors.push(CartFields.Title);
    }

    if (!validateNotBlank(cart.type)) {
      errors.push(CartFields.Type);
    }
  }

  return errors;
};
