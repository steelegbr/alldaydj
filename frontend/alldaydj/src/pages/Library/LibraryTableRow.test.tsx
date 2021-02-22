import React from 'react';
import { mount } from 'enzyme';
import { CartSearchResult } from '../../api/models/Search';
import LibraryTableRow from './LibraryTableRow';

const sampleResult : CartSearchResult = {
  id: '957dbe30-007d-442e-975e-42e096e60fa2',
  label: 'abc123',
  title: 'Cart Title',
  artist: 'Artist Name',
  year: 1988,
};

describe('library table row', () => {
  const getComponent = (result: CartSearchResult) => mount(<LibraryTableRow result={result} />);

  it('renders single result', () => {
    const component = getComponent(sampleResult);
    expect(component).toMatchSnapshot();
  });
});
