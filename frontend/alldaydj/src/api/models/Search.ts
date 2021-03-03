export interface CartSearchResult {
    label: string,
    id: string,
    title: string,
    artist: string,
    year: number
}

export interface CartSearchResults {
    count: number,
    next?: string,
    previous?: string,
    results: CartSearchResult[]
}

export type CartSearchConditionFields = 'advanced' | 'search' | 'artist' | 'title' | 'page' | 'resultsPerPage';

export type CartSearchConditions = Record<CartSearchConditionFields, string>;
