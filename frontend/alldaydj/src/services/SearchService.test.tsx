import { paramsToSearchConditions } from 'services/SearchService';

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
});
