from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, tokenizer

from alldaydj.models import Cart

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(number_of_shards=1, number_of_replicas=1)

ALLDAYDJ_ANALYZER = analyzer(
    "alldaydj",
    tokenizer="standard",
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
