from django_elasticsearch_dsl_drf.filter_backends.search.base import (
    BaseSearchFilterBackend,
)

from django_elasticsearch_dsl_drf.filter_backends.search.query_backends.match_phrase import (
    MatchPhraseQueryBackend,
)


class MatchPhraseFilterBackend(BaseSearchFilterBackend):
    """Match Phrase Backend"""

    query_backends = [MatchPhraseQueryBackend]
