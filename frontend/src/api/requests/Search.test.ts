import mockAxios from 'jest-mock-axios';
import { cartSearch } from 'api/requests/Search';
import { getTokenFromLocalStorage } from 'services/AuthenticationService';

const mockToken = getTokenFromLocalStorage as jest.Mock;
jest.mock('services/AuthenticationService');

describe('cart search', () => {
  beforeEach(() => {
    mockAxios.reset();
  });

  it('basic search', async () => {
    mockToken.mockReturnValue('TOKEN123');

    cartSearch({
      page: '1',
      resultsPerPage: '10',
      search: 'test',
    });

    expect(mockAxios.get).toBeCalledWith('/api/cart/search/', { headers: { Authorization: 'Bearer TOKEN123' }, params: expect.any(URLSearchParams) });
  });
});
