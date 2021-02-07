from haystack import indexes
from alldaydj.models import Cart


class CartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    artist = indexes.CharField(model_attr="display_artist")
    title = indexes.CharField(model_attr="title")
    label = indexes.CharField(model_attr="label")
    year = indexes.IntegerField(model_attr="year")

    def get_model(self):
        return Cart

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
