from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from alldaydj.models import Cart

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(number_of_shards=1, number_of_replicas=1)

CASE_INSENSITIVE_ANALYZER = analyzer(
    "case_insensitive",
    tokenizer="keyword",
    filter=["lowercase", "stop", "snowball"],
)


@INDEX.doc_type
class CartDocument(Document):
    id = fields.KeywordField(attr="id")
    title = fields.KeywordField(
        analyzer=CASE_INSENSITIVE_ANALYZER,
        fields={
            "raw": fields.TextField(analyzer="keyword"),
        },
    )
    artist = fields.KeywordField(
        analyzer=CASE_INSENSITIVE_ANALYZER,
        attr="display_artist",
        fields={
            "raw": fields.TextField(analyzer="keyword"),
        },
    )
    label = fields.KeywordField(
        analyzer=CASE_INSENSITIVE_ANALYZER,
        fields={
            "raw": fields.TextField(analyzer="keyword"),
        },
    )
    year = fields.IntegerField()

    class Django(object):
        model = Cart
