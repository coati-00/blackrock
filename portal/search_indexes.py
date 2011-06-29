import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import MultiValueField, CharField
from portal.models import *

class AssetIndex(SearchIndex):
  text = CharField(document=True, use_template=True)
  name = CharField(model_attr='name')
  study_type = MultiValueField(faceted=True)
  species = MultiValueField(faceted=True)
  discipline = MultiValueField(faceted=True)
  asset_type = CharField(faceted=True)
  infrastructure = MultiValueField(faceted=True)
  featured = MultiValueField(faceted=True)
  
  def prepare_study_type(self, obj):
    return [facet.name for facet in obj.facet.filter(facet='Study Type')]

  def prepare_species(self, obj):
    return [facet.name for facet in obj.facet.filter(facet='Species')]

  def prepare_discipline(self, obj):
    return [facet.name for facet in obj.facet.filter(facet='Discipline')]
    
  def prepare_infrastructure(self, obj):
    return [facet.name for facet in obj.facet.filter(facet='Infrastructure')]
  
  def prepare_asset_type(self, obj):
    return obj._meta.object_name

  def prepare_featured(self, obj):
    return [facet.name for facet in obj.facet.filter(facet='Featured')]
   
site.register(Station, AssetIndex)
site.register(Person, AssetIndex)
site.register(DataSet, AssetIndex)
site.register(ResearchProject, AssetIndex)
site.register(LearningActivity, AssetIndex)
site.register(ForestStory, AssetIndex)

from django.contrib import databrowse

databrowse.site.register(Station)
databrowse.site.register(Person)
databrowse.site.register(DataSet)
databrowse.site.register(ResearchProject)
databrowse.site.register(LearningActivity)
databrowse.site.register(ForestStory)

databrowse.site.register(Facet)
databrowse.site.register(Tag)


