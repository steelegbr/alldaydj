"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from os import environ
from typing import Dict, List

tokenizer = RegexpTokenizer(r"\w+")
language = environ.get("ADDJ_TOKEN_LANG", "english")
stemmer = SnowballStemmer(language, ignore_stopwords=True)


def fields_to_tokens(fields: List[str]) -> List[str]:
    # Get a list of unique tokens

    all_tokens = [tokenizer.tokenize(field) for field in fields]

    flattened_tokens = [
        token for token_sublist in all_tokens for token in token_sublist
    ]

    # Stem the words

    stemmed_tokens = set([stemmer.stem(token) for token in flattened_tokens])

    # Send the unique values back

    return list(stemmed_tokens)


def fields_to_weighting_map(fields: List[str]) -> Dict[str, int]:
    tokens = fields_to_tokens(fields)
    return Counter(tokens)
