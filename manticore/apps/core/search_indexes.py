import datetime

from haystack import indexes
from haystack import site

from .models import Category


class CategoryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')


site.register(Category, CategoryIndex)
