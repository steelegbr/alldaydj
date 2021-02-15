export interface CartSearchResult {
    label: String,
    id: String,
    title: String,
    artist: String,
    year: Number
}

export interface CartSearchResults {
    count: Number,
    next?: String,
    previous?: String,
    results: CartSearchResult[]
}

export type SearchConditionFields = 'advanced' | 'search' | 'artist' | 'title';

export type SearchConditions = Record<SearchConditionFields, string>;
