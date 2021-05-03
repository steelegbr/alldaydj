import { cartSearchContextFromQueryString, paramsToSearchConditions } from 'services/SearchService';

describe('cart search service', () => {
  it('querystring params to search conditions empty', () => {
    const converted = paramsToSearchConditions(new URLSearchParams());
    expect(converted).toStrictEqual({
      page: '1',
      resultsPerPage: '10',
      search: '',
    });
  });

  it('querystring params to search conditions valid', () => {
    const params : Record<string, string> = {
      page: '5',
      resultsPerPage: '7',
      search: 'something',
    };
    const converted = cartSearchContextFromQueryString(new URLSearchParams(params));
    expect(converted).toStrictEqual(
      {
        conditions: {
          page: '5',
          resultsPerPage: '7',
          search: 'something',
        },
        status: 'ReadyToSearch',
      },
    );
  });
});
