from haystack import indexes
from haystack import site

from .models import Profile


class ProfileIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)

site.register(Profile, ProfileIndex)
