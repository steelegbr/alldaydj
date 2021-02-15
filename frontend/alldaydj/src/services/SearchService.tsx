import { SearchConditions } from '../api/models/Search';

// eslint-disable-next-line import/prefer-default-export
export const paramsToSearchConditions = (query: URLSearchParams) : SearchConditions => ({
  advanced: query.get('advanced') || 'false',
  search: query.get('search') || '',
  artist: query.get('artist') || '',
  title: query.get('title') || '',
});
