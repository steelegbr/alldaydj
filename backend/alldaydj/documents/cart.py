from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from alldaydj.models import Cart

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(number_of_shards=1, number_of_replicas=1)


@INDEX.doc_type
class CartDocument(Document):
    id = fields.TextField(attr="id")
    title = fields.TextField(fields={"raw": fields.KeywordField()})
    artist = fields.TextField(
        attr="display_artist", fields={"raw": fields.KeywordField()}
    )
    label = fields.TextField(fields={"raw": fields.KeywordField()})
    year = fields.IntegerField()

    class Django(object):
        model = Cart
