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

export interface CartSearchResult {
    label: string,
    id: string,
    title: string,
    artist: string,
    year: number
}

export interface CartSearchResults {
    count: number,
    next?: string,
    previous?: string,
    results: CartSearchResult[]
}

export type CartSearchConditionFields = 'search' | 'page' | 'resultsPerPage';

export type CartSearchConditions = Record<CartSearchConditionFields, string>;
