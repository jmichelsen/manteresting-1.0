from haystack import indexes
from haystack import site

from .models import Profile


class ProfileIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    name = indexes.CharField(model_attr='name', null=True)
    about = indexes.CharField(model_attr='about', null=True)
    location = indexes.CharField(model_attr='location', null=True)


site.register(Profile, ProfileIndex)
