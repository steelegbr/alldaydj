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
import { mount } from 'enzyme';
import { CartSearchResult } from 'api/models/Search';
import LibraryTableRow from 'pages/Library/LibraryTableRow';

const sampleResult : CartSearchResult = {
  id: '957dbe30-007d-442e-975e-42e096e60fa2',
  label: 'abc123',
  title: 'Cart Title',
  artist: 'Artist Name',
  year: 1988,
};

const mockPush = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
}));

describe('library table row', () => {
  const getComponent = (result: CartSearchResult) => mount(<LibraryTableRow result={result} />);

  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('renders single result', () => {
    const component = getComponent(sampleResult);
    expect(component).toMatchSnapshot();
  });

  it('renders single result expanded', () => {
    const component = getComponent(sampleResult);
    const expandButton = component.find("[data-test='result-expand']").first();
    expandButton.simulate('click');
    component.update();
    expect(component).toMatchSnapshot();
  });

  it('edit links to the correct page', () => {
    const component = getComponent(sampleResult);
    const expandButton = component.find("[data-test='result-expand']").first();
    expandButton.simulate('click');
    component.update();

    const editButton = component.find("button[data-test='button-edit']");
    editButton.simulate('click');
    expect(mockPush).toBeCalledWith('/cart/957dbe30-007d-442e-975e-42e096e60fa2');
  });
});
