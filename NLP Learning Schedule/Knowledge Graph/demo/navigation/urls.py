from django.urls import path
from . import views

app_name = 'navigation'

urlpatterns = [
    path('overview', views.overview, name='overview'),
    path('search/entity_relationship', views.entity_relationship, name='entity_relationship'),
    # path('search/entity_to_entity', views.entity_to_entity, name='entity_to_entity'),
    path('search/entity_atribute', views.entity_attribute, name='entity_attribute'),
    path('search/entity_table', views.entity_table, name='entity_table'),
    path('search/source', views.source, name='source'),
    path('search/stars',views.stars, name='stars'),
    path('search/autocomplete', views.autocomplete, name='autocomplete'),
    path('search/relationship_search', views.relationship_search, name='relationship_search'),
    path('search/attribute_autocomplete', views.attribute_autocomplete, name='attribute_autocomplete'),
    path('search/attribute_search', views.attribute_search, name='attribute_search'),
]
