from dialogos.models import Comment
import haystack


haystack.autodiscover()

class CommentIndex(haystack.indexes.SearchIndex):
    text = haystack.indexes.CharField(document=True, use_template=True)
    comment = haystack.indexes.CharField(model_attr='comment')
    author = haystack.indexes.CharField(model_attr='author')

    def index_queryset(self):
        return Comment.objects.filter(public=True)

    def should_update(self, instance, **kwargs):
        if instance.public:
            return True
        else:
            self.remove_object(instance, **kwargs)
            return False

haystack.sites.site.register(Comment, CommentIndex)
