"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

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

from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, tokenizer

from alldaydj.models import Cart

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(number_of_shards=1, number_of_replicas=1)

ALLDAYDJ_ANALYZER = analyzer(
    "alldaydj",
    tokenizer=tokenizer("trigram", "ngram", min_gram=3, max_gram=3),
    filter=["lowercase", "stop", "snowball"],
)


@INDEX.doc_type
class CartDocument(Document):
    id = fields.KeywordField(attr="id")
    title = fields.TextField(
        analyzer=ALLDAYDJ_ANALYZER,
        fields={
            "raw": fields.KeywordField(),
        },
    )
    artist = fields.TextField(
        analyzer=ALLDAYDJ_ANALYZER,
        attr="display_artist",
        fields={
            "raw": fields.KeywordField(),
        },
    )
    label = fields.TextField(
        analyzer=ALLDAYDJ_ANALYZER,
        fields={
            "raw": fields.KeywordField(),
        },
    )
    year = fields.IntegerField()

    class Django:
        model = Cart
