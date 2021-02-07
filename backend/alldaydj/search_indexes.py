from haystack import indexes
from alldaydj.models import Cart


class CartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    display_artist = indexes.CharField()
    title = indexes.CharField()
    label = indexes.CharField()
    year = indexes.IntegerField()

    def get_model(self):
        return Cart

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
