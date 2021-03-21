import { CartSearchConditions } from 'api/models/Search';
import { CartSearch } from 'components/context/CartSearchContext';

const parseNumber = (raw: string | null, defaultValue = 1): string => {
  const parsedInt = parseInt(raw || '', 10);
  if (Number.isNaN(parsedInt) || parsedInt <= 0) {
    return `${defaultValue}`;
  }
  return `${parsedInt}`;
};

export const paramsToSearchConditions = (query: URLSearchParams) : CartSearchConditions => ({
  advanced: query.get('advanced') || 'false',
  search: query.get('search') || '',
  artist: query.get('artist') || '',
  title: query.get('title') || '',
  page: parseNumber(query.get('page')),
  resultsPerPage: parseNumber(query.get('resultsPerPage'), 10),
});

export const cartSearchContextFromQueryString = (query: URLSearchParams): CartSearch => ({
  conditions: paramsToSearchConditions(query),
  status: 'ReadyToSearch',
});
