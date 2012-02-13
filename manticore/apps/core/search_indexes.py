from haystack import indexes
from haystack import site

from .models import Category, Workbench, Nail


class CategoryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

site.register(Category, CategoryIndex)


class WorkbenchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')


site.register(Workbench, WorkbenchIndex)


class NailIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description')


site.register(Nail, NailIndex)
