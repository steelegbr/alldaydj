import React from 'react';
import { mount } from 'enzyme';
import { CartSearchConditionFields } from '../../api/models/Search';
import CartSearchContext, { CartSearchContextType, CartSearchStatus } from '../../components/context/CartSearchContext';
import LibrarySearch from './LibrarySearch';

const mockPush = jest.fn();
const mockSetSearch = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush,
  }),
}));

describe('cart library search', () => {
  const getComponent = (
    conditions: Record<CartSearchConditionFields, string>,
    status: CartSearchStatus,
  ) => {
    const contextParams : CartSearchContextType = {
      search: {
        conditions,
        status,
      },
      setSearch: mockSetSearch,
    };
    return mount(
      <CartSearchContext.Provider value={contextParams}>
        <LibrarySearch />
      </CartSearchContext.Provider>,
    );
  };

  it('basic search', () => {
    const component = getComponent(
      {
        advanced: 'false',
        artist: '',
        page: '1',
        resultsPerPage: '10',
        search: '',
        title: '',
      },
      'NotStarted',
    );

    const searchBox = component.find("[data-test='input-search']").find('input');
    searchBox.simulate('change', { target: { value: 'Test' } });
    component.update();

    const searchButton = component.find("[data-test='button-search']").find('button');
    searchButton.simulate('submit');

    expect(mockSetSearch).toBeCalledTimes(2);
    expect(mockSetSearch).toBeCalledWith({
      conditions: {
        advanced: 'false',
        artist: '',
        page: '1',
        resultsPerPage: '10',
        search: 'Test',
        title: '',
      },
      status: 'NotStarted',
    });
    expect(mockSetSearch).toBeCalledWith({
      conditions: {
        advanced: 'false',
        artist: '',
        page: '1',
        resultsPerPage: '10',
        search: '',
        title: '',
      },
      status: 'ReadyToSearch',
    });
    expect(mockPush).toBeCalledWith({
      pathname: '/library/',
      search: '?advanced=false&artist=&page=1&resultsPerPage=10&search=&title=',
    });
  });

  it('search does not trigger when in loading state', () => {
    const component = getComponent(
      {
        advanced: 'false',
        artist: '',
        page: '1',
        resultsPerPage: '10',
        search: 'Test',
        title: '',
      },
      'Searching',
    );

    const searchButton = component.find("[data-test='button-search']").find('button');
    searchButton.simulate('submit');

    expect(mockSetSearch).not.toBeCalled();
    expect(mockPush).not.toBeCalled();
  });
});
