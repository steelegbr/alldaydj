import { cartSearchContextFromQueryString, paramsToSearchConditions } from 'services/SearchService';

describe('cart search service', () => {
  it('querystring params to search conditions empty', () => {
    const converted = paramsToSearchConditions(new URLSearchParams());
    expect(converted).toStrictEqual({
      advanced: 'false',
      artist: '',
      page: '1',
      resultsPerPage: '10',
      search: '',
      title: '',
    });
  });

  it('querystring params to search conditions valid', () => {
    const params : Record<string, string> = {
      advanced: 'true',
      artist: 'The Artist',
      page: '5',
      resultsPerPage: '7',
      search: 'something',
      title: 'A Title',
    };
    const converted = cartSearchContextFromQueryString(new URLSearchParams(params));
    expect(converted).toStrictEqual(
      {
        conditions: {
          advanced: 'true',
          artist: 'The Artist',
          page: '5',
          resultsPerPage: '7',
          search: 'something',
          title: 'A Title',
        },
        status: 'ReadyToSearch',
      },
    );
  });
});
