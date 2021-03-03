import mockAxios from 'jest-mock-axios';
import { cartSearch } from 'api/requests/Search';

describe('cart search', () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  it('basic search', async () => {
    cartSearch({
      advanced: 'false',
      artist: '',
      page: '1',
      resultsPerPage: '10',
      search: 'test',
      title: '',
    },
    'token123');

    expect(mockAxios.get).toBeCalledWith('/api/cart/search/', { headers: { Authorization: 'Bearer token123' }, params: expect.any(URLSearchParams) });
  });

  it('advanced search', async () => {
    cartSearch({
      advanced: 'true',
      artist: 'artist',
      page: '1',
      resultsPerPage: '10',
      search: 'test',
      title: 'title',
    },
    'token123');

    expect(mockAxios.get).toBeCalledWith('/api/cart/search/', { headers: { Authorization: 'Bearer token123' }, params: expect.any(URLSearchParams) });
  });
});
