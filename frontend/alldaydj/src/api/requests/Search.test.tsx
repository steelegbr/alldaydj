import mockAxios from 'jest-mock-axios';
import { cartSearch } from './Search';

describe('cart search', () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  it('basic search', async () => {
    await cartSearch({
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
    await cartSearch({
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
